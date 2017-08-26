# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 16:02:01 2016
Updated 23 Sep 2016

@author: michaelcurrin

This script includes a few functions to be used in the google_analytics_reports.py
script. The idea is that this mikes_toolbox.py script can be repurposed for other
scripts which also need date ranges, neat formatting for table data in the terminal, or 
for sending mails.
"""
import smtplib # used to access Gmail
from email.MIMEMultipart import MIMEMultipart # used to send mail
from email.MIMEText import MIMEText # used to send mail

import datetime
import time

# download the original prettytable.py file from https://pypi.python.org/pypi/PrettyTable
# then place it in the same directory as mikes_toolbox.py before importing it
from prettytable import PrettyTable 


def PrintFinishedTables(listOfTables, reportSummary):
    """
    Iterate through a list of tables as input from the GetAnalyticsData method.
    Print them with neat spacing.
    """
    print reportSummary
    
    for site_segment_pairs in listOfTables:
        for tables in site_segment_pairs:
            print tables # or tables.get_string()
            print ''
            

def sendMail(body, inputSubject, fromAddr, toAddr, emailPassword):
    """
    Args
        body: single string, separated by '\n' breaks. 
                To use lists, input as '\n'.join(['first line', 'second line'])
        inputSubject: string. subject of mail
        fromAddr: string. sending address
        toAddr: string. receipient address
        emailPassword: string.
    Returns
        msg: full mail details
    """
    msg = MIMEMultipart('alternative')
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = inputSubject

    # create two iamges to be inserted at the top of the HTML mail

    # brand logo
    image1 = '<img src=http://deadline.com/2016/07/rupauls-drag-race-renewed-season-9-fire-island-kelly-ripa-logo-1201789160/" alt="logo"/>'

    # platform logo
    image2 = '<img src="https://developers.google.com/analytics/images/terms/logo_lockup_analytics_icon_vertical_black_2x.png" alt="GA" width="75"/>'

    
    # Create html message with font formatting 
    # and breaks for new lines
    # and %20 for spaces
    html = """\
    <html>
        <head>
            %s %s
            <font face="Courier New, Courier, monospace",font size="+2">
            <p>%s</p>
            </font>
        </head>
        <body> 
             <font face="Courier New, Courier, monospace", font size="+1"> <p>%s</p>
             </font>
        </body>
    </html>""" % (image1, image2, inputSubject, body.replace('\n','<br>').replace(' ','&nbsp;'))
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(fromAddr, emailPassword)
    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()
    
    return msg



def EmailFinishedTables(listOfTables, inputSubject, fromAddress, toAddressList, 
                        emailPassword):
    """
    Iterate through a list of tables as input from the GetAnalyticsData method.
    Combine them a text object list, with a new line for each line of the mail.
    Send mail using config credentials.
    
    Args
        listOfTables: list. Each item contains a single element or a tuple of 
                        two tables paired. This is converted to html for 
                        use of fonts.
        inputSubject: string. Subject of email
        fromAddress: string. from address to login with
        toAddressList: list of email address strings to send to
        emailPassword: string. password to go with fromAddr account
    """
    mailRows = []
    for sections in listOfTables:
        # go through tuple
        for tables in sections:
            # split by \n so table doesn't become one string
            mailRows += tables.get_string().split('\n')
            mailRows += ['']
            
    # create single string using all rows list elements 
    body = '\n'.join(mailRows)
    
    print 'Subject: %s' % inputSubject
    for toAddr in toAddressList:
        sendMail(body, inputSubject, fromAddress, toAddr, emailPassword)
        print 'Sent to: %s' % toAddr
    
    
def formatTable(headerFormatted, rowValues, setBorder = True, setAlign = 'r'):
    """
    Format a set of header and row values, using PrettyTable libary. 
    Align all columns to the right.
    
    Args
        headerFormatted: list
        rowValues: list, where each row is a list of column values for that row
        setBorder: True or False. Default to True.
        setAlign: 'l', 'r' or 'c'. Default is right.
    Returns
        table: formatted PrettyTable object
    """    
    prettyTable = PrettyTable()
    prettyTable.field_names = headerFormatted
    for rowData in rowValues:
        prettyTable.add_row(rowData)        
    prettyTable.align = setAlign
    prettyTable.border = setBorder
    return prettyTable     
 

def GetLast7DaysYesterday():
    """
    Set date range as 7 days before yesteday up to yesterday
    
    Returns
        startDate: date object. Start of period. 
        endDate: date object. End of period.
        countOfDays: integer. Number of days between start and end date
    """ 
    # today's date as the time of running the script
    today = datetime.date.today()
    
    # length of one day, in timedelta format
    oneDay = datetime.timedelta(days=1)
    
    # set end date as yesterday, start date 7 days before
    endDate = today - oneDay
    startDate = endDate - 6*oneDay
    
    countOfDays = endDate - startDate + oneDay
    
    return startDate, endDate, countOfDays
    
def GetLast7DaysToday():
    """
    Set date range as max 7 days, starting 7 days before today and ending 
    today.
    If the current time is 12pm then it will include 6 days and a half days.
    

    Returns
        startDate: date object. Start of period. 
        endDate: date object. End of period.
        countOfDays: integer. Number of days between start and end date
    """ 
    # today's date as the time of running the script
    today = datetime.date.today()
    
    # length of one day, in timedelta format
    oneDay = datetime.timedelta(days=1)
    
    # set end date as today, start date as 7 days before today
    endDate = today 
    startDate = endDate - 6*oneDay
    
    countOfDays = endDate - startDate + oneDay
    
    return startDate, endDate, countOfDays   

    
def GetMonthToDateRange():    
    """
    Set date range as start of yesterday's month up to yesterday's date. 
    Note that if today is the 2nd of the month and yesterday was the 1st, 
    then range will be from and to the 1st of this month (1 day only).
    
    Returns
        startDate: date object. Start of period. 
        endDate: date object. End of period.
        countOfDays: integer. Number of days between start and end date
    """ 
    # today's date as the time of running the script
    today = datetime.date.today()
    
    # length of one day, in timedelta format
    oneDay = datetime.timedelta(days=1)
    
    # set end date as yesterday, start date as the 1st day of yesterday's month
    endDate = today - oneDay
    startDate = datetime.date(endDate.year, endDate.month, 1)
    
    countOfDays = endDate - startDate + oneDay
    
    return startDate, endDate, countOfDays


def testMail():    
    # test mail functionality. this requires password to be entered

    body = """
    Site   Segment   
    Lumen  All Users 
    
    +-----------------+----------+---------+------------------+
    | channelGrouping | sessions | bounces | goal8Completions |
    +-----------------+----------+---------+------------------+
    |          Direct |        8 |       5 |                0 |
    |           Email |        5 |       1 |                0 |
    |  Organic Search |        2 |       0 |                0 |
    |          Social |        1 |       1 |                0 |
    | =============== | ======== | ======= | ================ |
    |                 |       16 |       7 |                0 |
    +-----------------+----------+---------+------------------+
    
     Site   Segment           
     Lumen  Returning Visitor 
    
    +-----------------+----------+---------+------------------+
    | channelGrouping | sessions | bounces | goal8Completions |
    +-----------------+----------+---------+------------------+
    |           Email |        1 |       0 |                0 |
    | =============== | ======== | ======= | ================ |
    |                 |        1 |       0 |                0 |
    +-----------------+----------+---------+------------------+]
    """ 
    inputSubject = 'Test'
    fromAddr = 'XXX@XXX.com'
    toAddr = 'XXXX@XXX'
    
    # Continue asking for the user for a password or 'X' to exit
    while True:
        print "Mail %s> " % fromAddr
        emailPassword = raw_input("Enter password or press Enter to ignore > ")
        
        #exit with blank inut or 'X'
        if emailPassword.upper() == 'X' or emailPassword.upper() == '':
            print ''            
            break
        
        #attempt to send mail and show error
        try:
            print sendMail(body, inputSubject, fromAddr, toAddr, emailPassword)
            break
        except:
            print '...'
            print 'Error - try again!'
            print '...'
            # sleep 2 seconds
            time.sleep(2)
            print ''
        
def testDates():
    dateDict = dict(GetLast7DaysYesterday=GetLast7DaysYesterday(),
                    GetLast7DaysToday=GetLast7DaysToday(),
                    GetMonthToDateRange=GetMonthToDateRange())
                     
    for ranges in dateDict:
        print ranges
        for items in dateDict[ranges]:         
            print str(items)
        print ''
        
    # example output where today was the 7th of July
    """
    GetMonthToDateRange
    2016-07-01
    2016-07-06
    6 days, 0:00:00
    
    GetLast7DaysToday
    2016-07-01
    2016-07-07
    7 days, 0:00:00
    
    GetLast7DaysYesterday
    2016-06-30
    2016-07-06
    7 days, 0:00:00
    """
   
    
if __name__ == '__main__':
    # run tests if this is the main script
    testMail()
    testDates()
