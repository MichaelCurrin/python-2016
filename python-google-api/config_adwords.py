#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:15:53 2016

@author: michaelcurrin

Values for config file on startup
"""
import datetime

def monthdelta(date, delta):
    """
    Test with 
      monthdelta((2016,11,10),-2)
      OR GetMonthToDate(-1,-2)
    from
        http://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python
    """
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)


def GetMonthToDate(end_offset_days=0, start_offset_months=0, out_format=''):
    """
    Return start and end dates for a period
    Where end date is the X days before/after today if offset is set.
    And start date is the first day of the end date's month.
    If end date is the 1st of the month, then start date will be the same date.

    Args
        end_offset_days: optional integer.
                        Defaults to 0 for today.
                        Set to -1 for yesterday.
        start_offset_months: optional integer
                        Defaults to 0 for start of current month (relative
                          to end date)
                        Set to -3 for 3 months before.        
        format: optional string.
                Default to '' to ignore formatting and return
                dates as date objects.
                Otherwise, use  '%Y%m%d' for YYYYMMDD output
                                '%Y-%m-%d' for YYYY-MM-DD output
                                etc.
    Returns
        start_date: start of period. Either as date object or as string
                    using format input if set.
        end_date: end of period. Either as date object or as string
                    using format input if set.
    """
    today = datetime.date.today()

    # set as X days before today
    end_date = today + datetime.timedelta(days=end_offset_days)

    # set as Y months before end date
    start_date = monthdelta(end_date,start_offset_months)
    # set as first day of month
    start_date = datetime.date(start_date.year, start_date.month, 1)

    if out_format:
        start_date = start_date.strftime(out_format)
        end_date = end_date.strftime(out_format)
    return start_date, end_date

################################################################################
### GOOGLE ADWORDS API
################################################################################

# name and ID are taken from Adwords manager account.
# title is  used for naming CSV downloads
adwords_accounts = [dict(name='XXXX', id='XXX-XXX-XXX',title='XXX')
                   #...
                   #...
                    
                    
                   #... 
                   ]

ADWORDS_VSN = 'v201605' # version of API to use

OUT_FORMAT = '%Y%m%d' # YYYYMMDD

# The past month from 1st up to 2 days ago.
START_DATE, END_DATE = GetMonthToDate(end_offset_days=-2,
                                      out_format=OUT_FORMAT)

# The past 3 months from 1st of month up to yesteday.
START_DATE_ALT, END_DATE_ALT = GetMonthToDate(end_offset_days=-1,
                                              start_offset_months=-2,
                                              out_format=OUT_FORMAT)
DATE_RANGE = '%s,%s' % (str(START_DATE), str(END_DATE))
DATE_RANGE_ALT = '%s,%s' % (str(START_DATE_ALT), str(END_DATE_ALT))

# directory of yaml file with Adwords credentials
# leave as '' to access /Users/michaelcurrin/googleads.yaml
# Note: NO " or \ is required to escape a white space character
YAML_LOCATION = '/Users/michaelcurrin/Google Drive/Cron/Authorisation/googleads.yaml'

# Queries written in AWQL
#   Order as SELECT...FROM...WHERE...DURING...
#   From documentation, ORDER BY and LIMIT are not supported
adwords_queries = [dict(name='campaign_report_totals',
                        select="""SELECT
                                  AccountDescriptiveName,
                                  CampaignStatus,
                                  CampaignId,
                                  CampaignName,
                                  AccountCurrencyCode,
                                  Amount,
                                  Period,
                                  ServingStatus,
                                  Cost,
                                  Impressions,
                                  Clicks,
                                  ConvertedClicks,
                                  Conversions,
                                  AllConversions,
                                  AveragePosition,
                                  AdNetworkType2
                              FROM CAMPAIGN_PERFORMANCE_REPORT
                              DURING %s""" % DATE_RANGE,
                        start_date=START_DATE,
                        end_date=END_DATE
                        # 3 month query split by day up to yesterday
                        ),
                    dict(name='campaign_report_by_day',
                        select="""SELECT
                                  Date,
                                  AccountDescriptiveName,
                                  CampaignStatus,
                                  CampaignId,
                                  CampaignName,
                                  AccountCurrencyCode,
                                  Amount,
                                  Period,
                                  ServingStatus,
                                  Cost,
                                  Impressions,
                                  Clicks,
                                  ConvertedClicks,
                                  Conversions,
                                  AllConversions,
                                  AveragePosition,
                                  MonthOfYear,
                                  AdNetworkType2
                              FROM CAMPAIGN_PERFORMANCE_REPORT
                              DURING %s""" % DATE_RANGE_ALT,
                        start_date=START_DATE_ALT,
                        end_date=END_DATE_ALT
                        # current MTD query as summary, up to 2 days ago
                        )
                    ]
"""
NOTES for adwordsSelectQueries
    ConvertedClicks: note this is deprecated is recenet API versions
    CampaignStatus: enabled, paused
    Camapign serving status: eligible
    Amount: Budget
    Period: Budget
    Alt columns
        ClickAssistedConversions
        Date (YYYY-MM-DD) which returns labeled as "Day"
"""
