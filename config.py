#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:15:53 2016

@author: michaelcurrin

Values for config file on startup
"""

# version of API to use
adwordsVsn = 'v201605'

# Query written in AWQL
adwordsSelectQueries = [dict(select="""SELECT
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
                                      AllConversions
                                  FROM CAMPAIGN_PERFORMANCE_REPORT
                                  DURING %s""",

                        # name to be used for CSV output
                        name='campaign_report',

                        # number of days before today to use as end date
                        offset= -2)]
"""
NOTES for adwordsSelectQueries
    ConvertedClicks: note this is deprecated is recenet API versions
    CampaignStatus: enabled, paused
    Camapign serving status: eligible
    Amount: Budget
    Period: Budget
    Alt columns
        ClickAssistedConversions
        Date (YYYY-MM-DD)
"""
