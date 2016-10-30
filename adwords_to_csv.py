#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created Oct 2016
@author: michaelcurrin

Download a CSV report from Adwords API for month to date. 

The script requires 
	live Adwords ad data, 
	a mananager account above the ad client account
	and a .yml file in the home directory containing authentication data
	a config.py file present in the working directory with the query data and 
		report name
	a directory called 'data' within the current working directory
This script asssumes all of those have been done.

This script is based on this article
	https://developers.google.com/adwords/api/docs/samples/python/reporting#download-a-criteria-performance-report-with-awql

Usage:
# e.g. 1
from adwords_to_csv.py import GetCampaignData
GetCampaignData()

# e.g. 2
or run adwords_to_csv.py directly
"""
from googleads import adwords
import datetime
import config


def GetMonthToDate(offset=0, format=''):
    """
    Return start and end dates for a period
    Where end date is the X days before/after today if offset is set.
    And start date is the first day of the end date's month.
    If end date is the 1st of the month, then start date will be the same date.

    Args
        offset: optional integer.
                Default to0 for today.
                Set to -1 for yesterday.
        format: optional string.
                Default to '' to ignore formatting and return
                dates as date objects.
                Otherwise, use  '%Y%m%d' for YYYYMMDD output
                                '%Y-%m-%d' for YYYY-MM-DD output
                                etc.
    Returns
        startDate: start of period. Either as date object or as string
                    using format input if set.
        endDate: end of period. Either as date object or as string
                    using format input if set.
    """
    today = datetime.date.today()
    endDate = today + datetime.timedelta(days=offset)
    startDate = datetime.date(endDate.year, endDate.month, 1)
    if format:
        startDate = startDate.strftime(format)
        endDate = endDate.strftime(format)
    return startDate, endDate

def GetAdwordsData(client, path, report_query, version='v201609'):
    """
    Query the Adwords API and download CSV reports

    Args
        client: authorised connection
        path: location of file to write to.
        reporty_query: query string for data required from API.
        				format using AWQL
							SELECT {variables names}
							FROM {report name}
							DURING {period length}
        				example
        					SELECT Date, Impressions
							FROM KEYWORD_PERFORMANCE_REPORT
							DURING LAST_30_DAYS
    """
    # Initialize downloader service.
    report_downloader = client.GetReportDownloader(version=version)

    try:
        # write out to CSV
        with open(path, 'w') as output_file:
            report_downloader.DownloadReportWithAwql(report_query,
                                                     'CSV',
                                                     output_file,
                                                     skip_report_header=True,
                                                     skip_column_header=False,
                                                     skip_report_summary=True)
        print 'Report was downloaded to \'%s\'.' % path
    except IOError as e:
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        print 'for path \t%s' % path
        print
    except:
        import sys
        print 'Unexpected error: ', sys.exc_info()[0]
        print 'for path \t%s' % path
        print

def main():
    """
	Read config file preferences,

    Set paths to write for
        CSV to overwrite existing file
        a new CSV file in the log subfolder

	Read data from Adwords API using credentials YAML (.yml) file in user
	home directory (otherwise, you're forced to open browser dialog to 
	create the file).
	Store reports as 2 CSVs.
    """
    # Initialize client object.
    adwords_client = adwords.AdWordsClient.LoadFromStorage()

    for report in config.adwordsSelectQueries:
        startDate, endDate = GetMonthToDate(offset=report['offset'],
                                            format='%Y%m%d')

        # CSV to overwrite existing file
        fileName1 = 'data/%s.csv' % report['name']

        # a new CSV file in the log subfolder
        fileName2 = 'data/log/%s_%s-%s.csv' % (report['name'], startDate,
                                               endDate)
        outfiles = [fileName1,fileName2]

        # set YYYYMMDD dates for query
        dateRange = '%s,%s' % (str(startDate), str(endDate))

        # use select query from config file and insert dates
        full_report_query = report['select'] % dateRange

        # read API version from config
        version = config.adwordsVsn

        # Download and write data to locations
        # (Please ensure /Users/michaelcurrin/googleads.yaml exists for
        # authorisation to succeed.)
        for path in outfiles:
            GetAdwordsData(adwords_client, path, full_report_query,
                               version=version)

if __name__ == '__main__':
    main()
