#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 16:23:50 2016

@author: michaelcurrin

Demonstrate use of public and insights data on Facebook Graph API
"""
import urllib2
import json
import datetime

### Build URLs ###


def FacebookPostsURL_user(userID, startDate, endDate, FBtoken):
    until = str(endDate + datetime.timedelta(days=1))
    graphURL = (
        "https://graph.facebook.com/v2.6/%s/posts?until=%s&limit=100&access_token=%s"
        % (userID, until, FBtoken)
    )
    return graphURL


def FacebookPostsURL_page(pageName, startDate, endDate, FBtoken):  # start date
    fields = "created_time,message,id,from,type"
    until = str(endDate + datetime.timedelta(days=1))
    graphURL = (
        "https://graph.facebook.com/v2.6/%s/posts?fields=%s&until=%s&limit=100&access_token=%s"
        % (pageName, fields, until, FBtoken)
    )
    return graphURL


def FacebookCountryFollowersURL(pageName, FBtoken):
    graphURL = (
        "https://graph.facebook.com/v2.6/%s/insights/page_fans_country?until=today&access_token=%s"
        % (pageName, FBtoken)
    )
    return graphURL


def FacebookGlobalFollowersURL(pageName, FBtoken):
    graphURL = "https://graph.facebook.com/v2.6/%s?fields=likes&access_token=%s" % (
        pageName,
        FBtoken,
    )
    return graphURL


def FacebookPageInsightsURL(pageName, FBtoken):
    graphURL = (
        "https://graph.facebook.com/v2.6/%s/insights/page_posts_impressions/days_28?access_token=%s"
        % (pageName, FBtoken)
    )
    return graphURL


#### Call API ###


def GetZAFollowers(pageName, FBtoken):
    graphURL = FacebookCountryFollowersURL(pageName, FBtoken)
    json_string = urllib2.urlopen(graphURL).read()
    parsed_json = json.loads(json_string)
    FB_data = parsed_json["data"]
    # print FB_data[0]['values'] # TEST

    try:
        length = len(FB_data[0]["values"])  # usually 3
        fans = FB_data[0]["values"][length - 1][
            "value"
        ]  # get most recent followers, last on the list
        fans = fans["ZA"]
    except:
        fans = -1
    return fans


def GetGlobalFollowers(pageName, FBtoken):
    graphURL = FacebookGlobalFollowersURL(pageName, FBtoken)
    json_string = urllib2.urlopen(graphURL).read()
    parsed_json = json.loads(json_string)

    fans = parsed_json["likes"]

    return fans


def GetInsights(pageName, FBtoken):
    graphURL = FacebookPageInsightsURL(pageName, FBtoken)
    json_string = urllib2.urlopen(graphURL).read()
    parsed_json = json.loads(json_string)

    data = parsed_json["data"]
    return data


def Main():
    """
    Demonstrate basic functionality of the script using 3 handles of pages on FB
    """
    # taken from https://www.facebook.com/pagehandle/'
    handles = ["ConstructiveEnlightenment", "bevan.soga", "WorldOfPuns"]

    # For quick access, to over to https://developers.facebook.com/tools/explorer/
    # Generate a short-lived token which expires within an hour
    # Paste it below
    FBtoken = "XXXXXXXXXXX"

    for handle in handles:
        print handle
        print GetInsights(handle, FBtoken)


if __name__ == "__main__":
    main()
