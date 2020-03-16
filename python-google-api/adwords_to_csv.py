#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created Oct 2016
@author: michaelcurrin

Download a CSV report from Adwords API for month to date. 

The script requires 
	live Adwords ad data, 
	a mananager account above the ad client account
	and a .yaml file in the home directory containing authentication data
    google ads installed 
        bash command
            $ sudo pip install googleads
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
import config_adwords as config


def GetAdwordsData(client, path, report_query, version="v201609"):
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
        with open(path, "w") as output_file:
            report_downloader.DownloadReportWithAwql(
                report_query,
                "CSV",
                output_file,
                skip_report_header=True,
                skip_column_header=False,
                skip_report_summary=True,
            )
        print "Saved -> %s" % path
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "for path \t%s" % path
        print
    except:
        import sys

        print "Unexpected error: ", sys.exc_info()[0]
        print "for path \t%s" % path
        print


def Main():
    """
	Read config file preferences,

    Set paths to write for
        CSV to overwrite existing file
        a new CSV file in the log subfolder

	Read data from Adwords API using credentials in YAML file in user
	home directory (otherwise, you're forced to open browser dialog to 
	create the file).
	Store reports as 2 CSVs.
    """

    # Get location of Adwords API credentials file
    YAML_LOCATION = config.YAML_LOCATION

    # API version number
    ADWORDS_VSN = config.ADWORDS_VSN

    # Pass credentials and initialize Adwords API client object
    adwords_obj = adwords.AdWordsClient.LoadFromStorage(YAML_LOCATION)

    adwords_accounts = config.adwords_accounts

    for account in adwords_accounts:
        print "Account: %s    ID: %s" % (account["name"], account["id"])
        # set account id for adwords object
        adwords_obj.SetClientCustomerId(account["id"])

        # download report for current account
        for report in config.adwords_queries:

            # read date range for each query
            start_date, end_date = report["start_date"], report["end_date"]

            # set names and directories for two identical files to be written
            constant_file = "data/%s_%s.csv" % (account["title"], report["name"])
            log_file = "data/history/%s_%s_%s-%s.csv" % (
                account["title"],
                report["name"],
                start_date,
                end_date,
            )
            out_files = [constant_file, log_file]

            query = report["select"]

            # Download and write data to locations
            for path in out_files:
                GetAdwordsData(adwords_obj, path, query, version=ADWORDS_VSN)
        print


if __name__ == "__main__":
    Main()
