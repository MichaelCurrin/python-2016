#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:15:53 2016

@author: michaelcurrin

Based on original file: https://developers.google.com/sheets/quickstart/python
Documentation: https://developers.google.com/sheets/guides/values

Note: Authorization information is stored on the file system, so subsequent
executions will not prompt for authorization.


Guide to Google Spreadsheets URL formats

URL: https://docs.google.com/spreadsheets/d/XXXXXXXXXX/edit#gid=YYYYYYYY
    The document or spreadsheet ID/key is XXXXXXXXXX.
    The worksheet id is YYYYYYYY and is independent of the sheet's name.
"""
import httplib2  # access www
import os # access to read/write files
import csv # read/write CSVs

# access Google Sheets API
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# script configuration use in Main()
import config

SCOPES = config.SCOPES
CLIENT_SECRET_FILE = config.CLIENT_SECRET_FILE
APPLICATION_NAME = config.APPLICATION_NAME

# this was in the original script
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

###############################################################################
# Table
###############################################################################

def ReadCSV(fileName):
    """
    Attempt to read a CSV file.
    if it fails, keep the list of rows empty

    Args
        fileName: string. e.g.  'test.csv'
        data: 2D list of rows and columns. cells could be strings or numerical.
            e.g.    [['A1', 'B1', 'C1'],
                     ['A2', 'B2', 'C2']]
    """
    data = []
    try:
        # 'rU' is needed because of errors reading some characters
        # U is for universal
        with open(fileName, 'rU') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    except:
        print 'Error reading file: %s' % fileName
    return data

def MakeEmptyTable(full_table):
    """
    Receive a table with values and return a version of the table with all
    values set to blank ('').

    Args
        values: 2D list of rows and columns
                e.g. values = [['a','bbbb','ccc'],
                               ['235235'],
                               ['325235235','dgdfg','fdgfdg']
    Returns
        emptyValues: 2D list of rows and columns set to ''.
                     e.g.  [['', '', ''],
                            [''],
                            ['', '', '']]
    """
    blank_table = []
    for row in full_table:
        blank_row = ['']*len(row)
        empty_values.append(blank_row)
    return empty_values

###############################################################################
# Authorise Sheets API
###############################################################################

def GetCredentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        credentials, the obtained credentials.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credentials_filename='sheets.googleapis.com-python-insights.json'
    credential_path = os.path.join(credential_dir,
                                   credentials_filename)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def GetService():
    credentials = GetCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service

#==============================================================================
# Read and write data with Sheets API
#==============================================================================

def GetGSheetsRange(service, spreadsheetId, range_name, printData=False):
    """Read data fom Google Spreadsheets using API.

    Args
        spreadsheet_ID: string. The long id taken from the URL of the file.
        range_name: string. Name of the sheet and range.
                    e.g. 'Sheet1!A1:E'
    Returns
        values: list of lists. The rows and columns read from the sheet.
    """
    service = GetService()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=range_name).execute()

    values = result.get('values', [])

    print 'READ RESULT'
    print
    for k, v in result.iteritems():
        if k!='values':
            print '%s: %s' % (k, v)

    if values:
        print '%i rows returned' % len(values)
    else:
        print 'No data returned!'
    print
    print

    if printData:
        print 'returned data...'
        print
        print range_name
        print '='*len(range_name)
        for row in values:
            for column in row:
                print column,
            print
        print

    return values

def WriteGSheetsRange(service, spreadsheetId, range_name, values,
                      value_input_option='RAW'):
    """Write data to Google Spreadsheets using API.

    Args
        service: authorised Sheets API object
        spreadsheet_ID: id of the docment to write to
        range_name: sheet name and cell reference if needed
        values: list of row and column values to write
        value_input_option: string. optional.
            either 'RAW' for conveting numbers and dates to text using '
            or 'USER_ENTERED' for normal formatting.
    """
    body = {'values':values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range=range_name,
        valueInputOption=value_input_option, body=body).execute()

    print 'WRITE RESULT'
    print
    for k, v in result.iteritems():
        print '%s: %s' % (k, v)
    print
    print

def OverwriteCells(service, spreadsheetId, sheet, newValues):
    """
    Read all cells in a sheet
    Overwrite them with blank values
    Write actual values.
    This prevents old values staying on the bottom part of thh sheet when
    only a few new rows are written at the top.
    """
    existingValues = GetGSheetsRange(service, spreadsheetId, sheet)
    emptyValues = MakeEmptyTable(existingValues)
    WriteGSheetsRange(service, spreadsheetId, sheet, emptyValues)
    WriteGSheetsRange(service, spreadsheetId, sheet, newValues,
                       value_input_option='USER_ENTERED')

def DeleteGSheetsRange(service, spreadsheetId, sheetId,
                       startIndex, endIndex, dimension='COLUMNS'):
    """Delete a range from a spreadsheet
    Note that references to cells which are deleted are not moved
    but become invlaid, as "=#REF!".
    """
    body = { "requests": [ {
                            "deleteDimension" : {
                                "range":{
                                  "sheetId": 0, # id  taken from gid=...
                                  "dimension": dimension,
                                  "startIndex": startIndex,
                                  "endIndex": endIndex
                                  #otherwise read from sheet first
                                }
                             }
                            }
                         ],
            }
    result = service.spreadsheets().batchUpdate(
                  spreadsheetId=spreadsheetId,
                  body=body).execute()

    print 'DELETE RESULT'
    print
    for k, v in result.iteritems():
        print '%s: %s' % (k, v)
    print
    print

###############################################################################
# Push data to Google Sheets from CSV
###############################################################################

def Main():
    """initially just hard code to write the campaign report"""
    # setup
    service = GetService()

    # read all sheets data from config
    sheetJobs = config.sheetUploadInstructions

    # iterate through job titles
    for title in sheetJobs.keys():
        uploadSheet = sheetJobs[title] # as ['campaign_report']

        # store data for specified CSV name
        fileName = ReadCSV(uploadSheet['sheetInput'])
        CSVdata = ReadCSV(fileName)

        OverwriteCells(service, uploadSheet['spreadsheetId'],
                       uploadSheet['sheetName'], CSVdata)

def Test():
    """run this script using test() for a demo of this script.
    Hardcoded values are used for data and sheet id"""

    # setup
    service = GetService()

    # doc: db_adwords
    spreadsheetId = '1d9Cb9-_-XTYHevDHUfVvQAZjJY9EN6yeZmEcR4DsFVw'

    # READ
    read_sheet = 'Sheet2' # please make sure this exists first
    read_data = GetGSheetsRange(service, spreadsheetId, read_sheet,
                    printData=True)
    print len(read_data)

    # WRITE
    write_sheet = 'Sheet1'
    newValues = [['a','bbbb','ccc'], ['235235'],['325235235','dgdfg','fdgfdg']]
    OverwriteCells(service, spreadsheetId, write_sheet, newValues)

    # DELETE
    DeleteSheetId = 2127202842
    DeleteGSheetsRange(service, spreadsheetId, DeleteSheetId, 1, 3)

if __name__ == '__main__':
    Main()
