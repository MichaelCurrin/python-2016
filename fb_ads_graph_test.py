#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
The purpose of this script is to test and showcase the ability to connect to FB Ads API
using the Facebook Graph API. It requires a FB Ads account or at least access
to a sandbox account.

The two output steps are
part 1: print the finished sample URLs with tokens added
part 2: print the results of API queries

The queries are based on queries in Klipfolio dashboard tool.

Next steps for possible improvements:
> decide how to use the URLs for reporting. make the URLs dynamic 
    (for any version, account, date range etc.)
> identify metrics and dimensions needed for the Media department's
  needs and apply them to queries.
> map standard JSON results into values to be used in a CSV report
 or database
> find out if any URls linking to ads or images can be returned from the API
"""
import urllib2
import json

def GetAdTest(url, FBtoken):
    """
    Read in a finished URL for Facebook Graph, 
    append a token, 
    run the query
    return the data

    Args
        url: string. A query string in the form 'https://graph.facebook.com/v2.7/accountid/...''
    Returns
        data: list or dictionary of API data returned for the query
    """
    graphURL = url + '&access_token='+ FBtoken
    json_string = urllib2.urlopen(graphURL).read()
    parsed_json = json.loads(json_string)
    data = parsed_json['data'] 
    return data

####################################################################################
# FLAT QUERIES
####################################################################################

# 5 URLs for accessing FB Ads data, all through FB graph API
# This negates the need for the FB Ads python module

# v2.7 is used below, since v2.6 is deprecated for ads and therefore produces an error message.

# URL for account
dailystats = 'https://graph.facebook.com/v2.7/act_701336110001704/insights?date_preset=last_7_days&time_increment=1&fields=account_id,cpm,cpp,spend,impressions,reach'

# URLS for campaign
adset_budget = 'https://graph.facebook.com/v2.7/6046949990398/adsets?fields=id,name,lifetime_budget,daily_budget,budget_remaining'
ad_campaign_metrics = "https://graph.facebook.com/v2.7/6046949990198/insights?time_range[since]=2016-07-01&time_range[until]=2016-07-20&time_increment=1&fields=spend,actions,ctr,clicks,impressions&limit=100"

# URLs for account
ad_metrics = 'https://graph.facebook.com/v2.7/act_701336110001704/insights?level=ad&fields=ad_name,adset_name,campaign_name,spend,unique_clicks,cost_per_unique_click,cpm,ctr&sort=spend_descending&date_preset=today'
active_campaigns = "https://graph.facebook.com/v2.7/act_701336110001704/campaigns?fields=id,name,created_time,effective_status&effective_status=['ACTIVE']"


urls = [dailystats, 
        adset_budget, 
        ad_campaign_metrics, 
        ad_metrics, 
        active_campaigns]


def Main():

    # FB token is generated in business manager, with ads access
    FBtoken = 'EAAIG7v8rtQUBANDmrBhvRf9InXxwwKH0mZBcZAnW4d038cZAlZA2osfdP4mUdGeeftZBcURwQ17VsEiZBTqWg33mTeWDNKiPYdQqpyhEomEJWA3VCZBMrnZBMnHMZCw58P7ZBXj4KBVZACBsYviuiFDo40Kto8XN918he4ZD'
     
    # Print URLs with token
    if True:
        for url in urls: 
            graphURL =  url+ '&access_token='+ FBtoken
            print graphURL
            print '***'
            # you can paste the URL this in your browser
            # recommended: install a pretty JSON viewer in your browser


    # Get API data and print
    if True:  
        
        for url in urls: 
            print url
            print '#####'    
            result = GetAdTest(url, FBtoken) 
            for row in result:
                print row
            print
            print '****************************'
            print

if __name__ == '__main__':
    main()


        
"""SAMPLE RESULTS

#1 dailystats
    {
        account_id: "701336110001XXX",
        cpm: 65.428933780234,
        cpp: 77.347397729707,
        spend: 722.27,
        impressions: "11039",
        reach: "9338",
        date_start: "2016-07-26",
        date_stop: "2016-07-26"
    },
    ...


#2 adset_budget
   [
    {
        id: "604694999XXXX",
        name: "Client ABC- Page Likes July 2016 - KEYWORDS",
        lifetime_budget: "700000",
        daily_budget: "0",
        budget_remaining: "123503"
    }
    ],  

    only for selected campaign     
   
   
   
#3 ad_campaign_metrics
   
   activity by day for a campaign queried
   {
        spend: 4.07,
        actions: [
        {
        action_type: "like",
        value: 2
        },
        {
        action_type: "page_engagement",
        value: 2
        }
        ],
        ctr: 2.9411764705882,
        clicks: "2",
        impressions: "68",
        date_start: "2016-07-08",
        date_stop: "2016-07-08"
    },
    {
        spend: 27.86,
            actions: [
            {
            action_type: "like",
            value: 23
            },
            {
            action_type: "photo_view",
            value: 1
            },
            {
            action_type: "post",
            value: 2
            },
            {
            action_type: "page_engagement",
            value: 26
            },
            {
            action_type: "post_engagement",
            value: 3
            }
            ],
        ctr: 6.9069069069069,
        clicks: "23",
        impressions: "333",
        date_start: "2016-07-09",
        date_stop: "2016-07-09"
    },
       
    
#4 ad_metrics
    
    # activity across campaigns
    here for the period was not set sp the value is today
{
    ad_name: "Client ABC - Page Likes – WITH ONE CARD – Go the distance",
    adset_name: "Client ABC - Page Likes July 2016 - NO TARGETING",
    campaign_name: "Client ABC - Page Likes July 2016 - NO TARGETING",
    spend: 92.31,
    unique_clicks: "46",
    cost_per_unique_click: 2.0067391304348,
    cpm: 46.155,
    ctr: 2.3,
    date_start: "2016-08-01",
    date_stop: "2016-08-01"
},
{
    ad_name: "Client ABC - Page Likes - WITH ONE CARD - Get in the Game",
    adset_name: "Client ABC - Page Likes July 2016 - LOOKALIKES",
    campaign_name: "Client ABC - Page Likes July 2016 - LOOKALIKES",
    spend: 88.78,
    unique_clicks: "44",
    cost_per_unique_click: 2.0177272727273,
    cpm: 53.034647550777,
    ctr: 2.7479091995221,
    date_start: "2016-08-01",
    date_stop: "2016-08-01"
},
...


#5 active_campaigns
{
    id: "6046949990598",
    name: "Client ABC - Page Likes July 2016 - NO TARGETING",
    created_time: "2016-07-08T16:19:52+0200",
    effective_status: "ACTIVE"
},
...

u'paging': {u'cursors': {u'after': u'NjA0MzgxMjMzMTU5OAZDZD',
u'before': u'NjA0Njk0OTk5MDU5OAZDZD'}}}
"""
