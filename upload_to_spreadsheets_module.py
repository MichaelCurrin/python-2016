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

# handle Google Sheet connection error
from googleapiclient import errors as google_errors

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
    # 'rU' is needed because of errors reading some characters
    # U is for universal
    with open(fileName, 'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

'''def MakeEmptyTable(full_table):
    """
    Receive a table with values and return a version of the table with all
    values set to blank ('').

    Args
        values: 2D list of rows and columns
                e.g. values = [['a','bbbb','ccc'],
                               ['235235'],
                               ['325235235','dgdfg','fdgfdg']
    Returns
        blank_table: 2D list of rows and columns set to ''.
                     e.g.  [['', '', ''],
                            [''],
                            ['', '', '']]
    """
    blank_table = []
    for row in full_table:
        blank_row = ['']*len(row)
        blank_table.append(blank_row)
    return blank_table'''

def MakeEmptyTable(in_table=[[]], row_count=0, column_count=0):
    """
    1 Read in *in_table*
    2 Create an empty table 
        of '' values,
        which has with the same number of rows and columns as the table,
        (where columns based on the first row).
    3 If the user has specified *row_count* and/or *column_count*,
        then these will be used place of the dimensions of *in_table*.
    
    Therefore *in_table* can be omitted from input if BOTH row_count and 
    column_count are set.
         e.g. MakeEmptyTable(row_count=1000, column_count=200)

    And if *in_table* is used, then the other 2 inputs are optional.
        e.g. MakeEmptyTable(CSVdata, row_count=1000)
            will use column_count of CSVdata but row_count as 1000

    Args
        in_table: <type 'list'> 2D table as list of lists, which may contain
                    table data in rows and columns.
                    e.g.    [['abc','def','hij'],
                            ['232','965','TES']
                            ['235','768','QWE']]
        row_count: <type 'int'> number of empty rows to create.
                    If this is not set, then in_table row count will be used.
        column_count: <type 'int'> number of empty columns to create in each
                        row.
                    If this is not set, then column count of *in_table* first
                        row  will be used.
    """
    if not row_count:
        row_count = len(in_table) # length of table

    if not column_count:
        column_count = len(in_table[0]) # length of first row of table

    row_contents = ['']*column_count # repeat '' for X columns
    blank_table = [row_contents]*row_count # repeat blank row for Y rows
    return blank_table

###############################################################################
# Authorise Sheets API
###############################################################################

def GetCredentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials
    are store them in hidden .credentials folder.

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

def GetGSheetsRange(service, spreadsheetId, range_name, test_print_rows=0,
                    quiet=True):
    """Read data fom Google Spreadsheets using API.

    Args
        spreadsheet_ID: string. The long id taken from the URL of the file.
        range_name: string. Name of the sheet and range.
                    e.g. 'Sheet1!A1:E'
        test_print_rows: integer. 
            e.g. 0 to not print (default) 
            e.g. 10 to print 10 rows
    Returns
        values: list of lists. The rows and columns read from the sheet.
    """
    
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=range_name).execute()

    values = result.get('values', [])

    if not quiet:
        print '  READ RESULT'
        for k, v in result.iteritems():
            if k is not 'values':
                print '   %s: %s' % (k, v)
    """
    # Example
    range: tb_staging_camp_perf!A1:Q1000
    majorDimension: ROWS
    152 rows returned  
    """
    if values:
        print '%i rows returned' % len(values)
    else:
        print 'No data returned!'
    print

    if not quiet:
        if test_print_rows:
            print_values = values[:test_print_rows]
            print 'printing %i rows...' % len(print_values)
            print
            print range_name # e.g. tb_staging_camp_day!A1:Z1000
            print '='*len(range_name)
            for row in print_values:
                print ','.join(row)
            print
    return values

def InsertGSheetsRows(service, spreadsheetId, range_name, values,
                      value_input_option='RAW', quiet=True):
    """Insert or append data to Google Spreadsheets using API.

    Args
        service: authorised Sheets API object
        spreadsheet_ID: id of the docment to write to
        range_name: sheet name and cell reference if needed
        values: list of row and column values to write
        value_input_option: string. optional.
            either 'RAW' for conveting numbers and dates to text using '
    """
    body = {
      'values': values
    }
    result = service.spreadsheets().values().append(
                    spreadsheetId=spreadsheetId, range=range_name,
                    valueInputOption=value_input_option, body=body).execute()
    print result

def WriteGSheetsRange(service, spreadsheetId, range_name, values,
                      value_input_option='RAW', quiet=True):
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

    if not quiet:
        print '  WRITE RESULT'
        for k, v in result.iteritems():
            print '    %s: %s' % (k, v)
        print
    """
    # example
    spreadsheetId: 1d9Cb9-_-XTYHevDHUfVvQAZjJY9EN6yeZmEcR4DsFVw
    updatedRange: tb_staging_camp_day!A1:O630
    updatedCells: 9450
    updatedRows: 630
    updatedColumns: 15
    """

def OverwriteCells(service, spreadsheetId, sheet, newValues, quiet=True):
    """
    Read all cells in a sheet
    Overwrite them with blank values to ensure sheet is empty
    Write actual values.

    This prevents old values staying on the bottom part of the sheet when
    only a few new rows are written at the top.
    Deleting rows or columns would unfortunately references from other sheets
    to that one, plus arrangment of other cells on that sheeg.
    """
    print 'Sheet:  %s' % sheet
    print 'Command:  Upload to sheets, overwriting data'
    try:
        print 'Reading existing values...'
        preview = 3
        existingValues = GetGSheetsRange(service, spreadsheetId, sheet,preview,
                                        quiet=quiet)
        print 'Emptying table...'
        emptyValues = MakeEmptyTable(existingValues)
        WriteGSheetsRange(service, spreadsheetId, sheet, emptyValues,
                            quiet=quiet)
        print 'Uploading new data...'
        WriteGSheetsRange(service, spreadsheetId, sheet, newValues,
                           value_input_option='USER_ENTERED',quiet=quiet)
        print 
        print 'Done.'
        
    except google_errors.HttpError as h:
        print 'ERROR'
        print ' - Http connection to Google Sheets failed!'
        print ' - %s' % h
    print
    print

def DeleteGSheetsRange(service, spreadsheetId, sheetId,
                       startIndex, endIndex, dimension='COLUMNS', quiet=True):
    """Delete a range from a spreadsheet
    Note that references to cells which are deleted are not moved
    but become invlaid, as "=#REF!".
    """
    body = { "requests": [ {
                            "deleteDimension" : {
                                "range":{
                                  "sheetId": sheetId, # id  taken from gid=...
                                  "dimension": dimension,
                                  "startIndex": startIndex, # starting from 0
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

    if not quiet:
        print 'DELETE RESULT'
        for k, v in result.iteritems():
            print '%s: %s' % (k, v)
        print

def Test():
    """run this script using test() for a demo of this script.
    Hardcoded values are used for data and sheet id"""

    #https://docs.google.com/spreadsheets/d/1CR_8w8ZYeu8gD9X3UwwtuZA2djj5jCpNSFycNSXM_GY/edit#gid=1608909088
    # setup
    
    service = GetService() 
    # - preface as upload.GetService() if use in another file

    # doc: db_adwords
    spreadsheetId = '1CR_8w8ZYeu8gD9X3UwwtuZA2djj5jCpNSFycNSXM_GY'

    # READ
    read_sheet = 'Sheet2' # please make sure this exists first
    read_data = GetGSheetsRange(service, spreadsheetId, read_sheet,
            quiet=False)
    print len(read_data)

    # WRITE
    write_sheet = 'Sheet1'
    newValues = [['a','bbbb','ccc'], ['235235'],['325235235','dgdfg','fdgfdg']]
    OverwriteCells(service, spreadsheetId, write_sheet, newValues,
        quiet=False)

    # DELETE
    DeleteSheetId = 1608909088
    DeleteGSheetsRange(service, spreadsheetId, DeleteSheetId, 0, 3,
        quiet=False)

if __name__ == '__main__':    
    Test() 
