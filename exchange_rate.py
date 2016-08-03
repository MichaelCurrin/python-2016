#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Fri July 22 2016

Author
    Michael Currin
    Twitter.com: @michaelcurrin
    Github.com: MichaelCurrin

Get Rand/Dollar exchange rate for a date or date range.
Using Fixer's API at http://api.fixer.io.
No account or API key is needed.

Documentation is available for the API at http://fixer.io.
Data values are sourced orignally from http://www.ecb.europa.eu/

I recommend using importing these methods, applying your currency and dates
then storing the date-value pairs in a database.
Let me know if this script comes in handy for anyone.
"""
import datetime
import urllib2 # access the web
import json # convert from JSON format into Python lists and dictionaries

#==============================================================================
# Date methods
#==============================================================================

def GetTodayString():
    """
    Return today's date as YYYY-MM-DD format
    """
    return str(datetime.date.today())
 
def ConvertStringToDate(dateString):   
    """
    Convert a date in string format to date object and return it.
    Args
        dateString: string in YYYY-MM-DD format
    Returns 
        dateObject: date object. e.g. datetime.date(2016,7,5)
    """
    dateObject = datetime.datetime.strptime(dateString,'%Y-%m-%d').date()
    return dateObject
    
def GetDateRange(startDate, endDate):
    """
    Args
        startDate: date object. e.g. datetime.date(2016,7,1))
        endDate: date object. e.g. datetime.date(2016,7,11)
    Returns
        dateRange: list of dates for period, in datetime.date format.
    """
    #calculate number of days in range
    oneDayMargin = datetime.timedelta(days = 1)
    countDays = endDate - startDate + oneDayMargin
    countDaysInt = countDays.days
    
    # create a list of each day from start to end date
    dateRange = [startDate + oneDayMargin*x for x in range(countDaysInt)]
    
    return dateRange


#==============================================================================
# Currency methods
#==============================================================================

def GetRateURL(base, symbols, date= 'latest'):
    """Create the URL needed to access the API.
    For a date and chosen currencies."""
    url = 'http://api.fixer.io/%s?base=%s&symbols=%s' % (date, base, symbols)
    return url   
    
def GetRateBaseSymbol(base, symbol, date= 'latest'):
    """
    Args
        base: string. e.g. USD. Name of original currency, as 3 characters        
        symbol: string e.g. ZAR. Name of conversion currency as 3 characters.
            Only one symbol is accepted and returned for this method,
            even though the API allows multiple comma separated symbols.
        date: string as YYYY-MM-DD format or the word 'latest'.
    Returns
        returnedDate: string. Date returned from query, even if set to latest.
        rate: decimal
        exchange: user-friedly display of conversation rate to 2 decimal places
    """
    # remove any additional characters after first symbol
    symbol = symbol[:3] 
    
    # get data from API
    url = GetRateURL(base, symbol, date)
    json_string = urllib2.urlopen(url).read()
    data = json.loads(json_string)
    
    # store returned date and currency rate
    returnedDate, rate = data['date'], data['rates'][symbol]
    
    # format exchange rate in easy to read string
    exchange = '1 %s = %s %s' % (base, round(rate,2), symbol)
    
    return returnedDate, rate, exchange
    
def GetRatesForRange(base, symbol, startDate, endDate):
    """
    Return pairs of dates and rates for a 2 currencies and given date range.
    Where start and end dates are datetime.date objects.
    """
    # create date range list
    dateRange = GetDateRange(startDate, endDate)
    
    # create a list of date and rate pairs by accessing the API for each day
    dailyRates = [GetRateBaseSymbol(base, symbol, str(date)) \
                                                    for date in dateRange]
                                                        
    # create a new list without duplicates
    # since the API sometimes returns an identical date and value combinations
    # for consecutive days.     
    dailyRatesDeDuped = []                                                    
    for value in dailyRates:
        if value not in dailyRatesDeDuped:
            dailyRatesDeDuped.append(value)
                                                    
    return  dailyRatesDeDuped


#==============================================================================
# Test this script
#==============================================================================

if __name__ == '__main__':
    base ='USD'
    symbol = 'ZAR'    
    
    print 'Testing exchange_rate.py and getting API data...'
    print
    print '***** TEST 1 *****'
    print "Most recent day available"
    print "(This may be yesterday's value if today is not in the API)"
    ZAR_data = GetRateBaseSymbol(base, symbol)
    for x in ZAR_data: 
        print x    
    
    print
    
    print '***** TEST 2 *****'
    print 'Date Range for %s to %s ' % (symbol, base)
    print 
    
    # use sample dates of 1 to 26 July as YYYY-MM-DD input
    startStr = '2016-07-01'
    endStr = '2016-07-26'
    start = ConvertStringToDate(startStr)
    end = ConvertStringToDate(endStr)

    # create list of data pairs
    dailyRates = GetRatesForRange(base, symbol, start, end)
    
    # print data
    for x in dailyRates:
        print x[0], x[1] # ignore 'exchange' in [x2] for testing

     
    # Sample output shown below
    """
    Testing exchange_rate.py and getting API data...

    ***** TEST 1 *****
    Most recent day available
    (This may be yesterday's value if today is not in the API)
    2016-08-02
    13.97
    1 USD = 13.97 ZAR
    
    ***** TEST 2 *****
    Date Range for ZAR to USD 
    
    2016-07-01 14.574
    2016-07-04 14.492
    2016-07-05 14.751
    2016-07-06 14.89
    2016-07-07 14.66
    2016-07-08 14.696
    2016-07-11 14.442
    2016-07-12 14.304
    2016-07-13 14.333
    2016-07-14 14.212
    2016-07-15 14.348
    2016-07-18 14.266
    2016-07-19 14.327
    2016-07-20 14.283
    2016-07-21 14.293
    2016-07-22 14.247
    2016-07-25 14.274
    2016-07-26 14.429    
    
    
    # Values prior to dupication removal method
    2016-07-01 14.574
    2016-07-01 14.574
    2016-07-01 14.574
    2016-07-04 14.492
    2016-07-05 14.751
    2016-07-06 14.89
    2016-07-07 14.66
    2016-07-08 14.696
    2016-07-08 14.696
    2016-07-08 14.696
    2016-07-11 14.442
    2016-07-12 14.304
    2016-07-13 14.333
    2016-07-14 14.212
    2016-07-15 14.348
    2016-07-15 14.348
    2016-07-15 14.348
    2016-07-18 14.266
    2016-07-19 14.327
    2016-07-20 14.283
    2016-07-21 14.293
    2016-07-22 14.247
    2016-07-22 14.247
    2016-07-22 14.247
    2016-07-25 14.274
    2016-07-26 14.429
    """
