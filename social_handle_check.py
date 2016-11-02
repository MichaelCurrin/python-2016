#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on 14 March 2016

@author: michaelcurrin

This script is intended to do a daily check of inputted Facebook and Twitter handles from a CSV file,
against the handles on Facebook API and Twitter API. 
The results are automatically emailed, including number of errors in the subject and the specific
errors marked in the output. This file is ideal for a cronjob schedule.

The idea is to pick up any brands which have changed their handles. 
If the brand handle is still correct, then it can be used for followers- or post-based query.

(If the fixed numerical ID of a FB page is used instead, then the FB queries would not be affected)
"""

import smtplib # used to access Gmail
from email.MIMEMultipart import MIMEMultipart # used to send mail
from email.MIMEText import MIMEText # used to send mail
import urllib2 # used to open FB graph queries
import oauth2 as oauth #used query Twitter API
import json # used to convert API JSON results to usable format
import datetime #used to display times and durations

# here are a few handles to get you started. replace them as necessary
FBInputCompetitorHandles = {'SetA': ['TEDEducation', 'ConstructiveEnlightenment','curiositydotcom'],
                           'SetB': ['WorldOfPuns', 'dyesciencebro'],
                            'DeliberateError':['abcxyz123xxx']
                          } 
TWInputCompetitorHandles = {'Health':['@CiplaRSA','@Novartis','@Pfizer_news'],
                            'Rice':['@SpekkoSA','@Tastic_Rice']
                           }

StartTime = datetime.datetime.now() # record start of program
print 'Started at %s' % str(StartTime)

# ---------EMAIL-------------------------------

addressList = ['user1@gmail.com','user2@yahoo.com'] # enter users you wish to send to


def sendMail(inputText,inputSubject,inputToAddress) : # method to send mail with defined text, subject and to address
    fromaddr = "myaccount@gmail.com" # replace with your gmail address
    toaddr = inputToAddress
    mypassword = 'password'

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = inputSubject

    body = inputText
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(fromaddr, mypassword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text) # customising the fromaddr as 'python' doesn't affect mail
    server.quit()



# ---------FACEBOOK SETUP-------------------------------


ManualExtendedToken = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# manually extended token
# Instructions
# 1 Go to https://developers.facebook.com/tools/accesstoken/#_=_
# 2 Generate USER token for your app
# 3 click "Debug"
# 4 click "Extend"
# 5 Copy and paste above.

# the expiry date should be for 2 months time.



#-------FACEBOOK METHODS------------------

def TestActiveToken(pageName, FBtoken):
    """check whether token is valid"""
    
    graphURL = 'https://graph.facebook.com/v2.5/%s?access_token=%s' % (pageName,FBtoken)

    try:
        urllib2.urlopen(graphURL).read() # test FB graph URL
        return 'OK','Token valid. Testing continued.'
    except:
        return 'Error', 'Warning - token not valid! Please extend your token and update it in the script.' #or put the token in a CSV file in the same folder and setup a way to read from that


def TestFBUserAbout(pageName,FBtoken):
    """check whether a page exists"""
    
    if pageName == 'n/a' or pageName == '' or pageName == '""': # return "OK" if the handle is n/a is empty
        result = 'OK'
    else:
        try:
            graphURL = 'https://graph.facebook.com/v2.7/%s?access_token=%s' %(pageName,FBtoken)
            json_string = urllib2.urlopen(graphURL).read() # test FB graph URL
            parsed_json = json.loads(json_string) # return name and ID
            FB_name, FB_id = parsed_json.values() # save results as FB page name and FB page id
            result = 'OK' # - name: %s     id:%s' % (FB_name, FB_id) #optional print page name and id
        except:
            result =  '---------------------------------Error!'
    return result



def FacebookCheck():
    """return list of success and failures for Facebook handles list, with total counts
    """
    FBMessageList = ['FACEBOOK TESTING\n']
    FBfound = 0
    FBmissing = 0

    TokenStatus,TokenTestMessage = TestActiveToken('MichaelCurrinPhotography', ManualExtendedToken) # check whether token works by testing URL for a controlled page
    FBMessageList.append(TokenTestMessage) # add token feedback message
    FBMessageList.append('\n')


    # continue to test handles if token is valid
    if TokenStatus == 'OK':

        for clientName in FBInputCompetitorHandles:   # look through client names

            str1= clientName  # e.g. Amstel
            FBMessageList.append(str1)

            for index in range(len(FBInputCompetitorHandles[clientName])): # look through handles in client
                str2= '    /%s' % FBInputCompetitorHandles[clientName][index] # e.g. /CastleLite
                str3 = TestFBUserAbout(FBInputCompetitorHandles[clientName][index],
                                       ManualExtendedToken) # e.g. OK or Error
                str4 = str2 + '    ' + str3 # e.g. /CastleLite OK
                FBMessageList.append(str4)

                if str3 =='OK': # add to the found or miss totals
                    FBfound += 1
                else:
                    FBmissing +=1

        FBsummary = '\n%i of %i FB pages found\n\n' % (FBfound,(FBfound + FBmissing)) # e.g. "30 of 36 FB pages found"
        FBMessageList.append(FBsummary)

    else:
        FBmissing = -1 #if token is not valid then FBmissing becomes -1

    FBMessage = '\n'.join(FBMessageList) # combine all FB message list values into single string with line breaks
    return FBMessage, FBmissing



#-------TWITTER SETUP------------------


# authorise Twitter API using registered app
CONSUMER_KEY = "XXXXX"
CONSUMER_SECRET = "XXXXX"
ACCESS_KEY = "XXXXX"
ACCESS_SECRET = "XXXXXXX"
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)


#-------TWITTER ACTIONS------------------


def TestActiveTwitterToken(handle):
    """
    check whether the token details are valid
    """
    
    try:
        twitterQuery = 'https://api.twitter.com/1.1/users/show.json?' + 'screen_name=' + handle
        T_response,json_string = client.request(twitterQuery)
        json_string = json.loads(json_string)
        error = json_string['errors'] #attempt to look for error message
        result =  'Error', error
    except:
        result = 'OK', 'Token is valid. Testing continued.\n'
    return result


def TwitterReturnUserExists(handle):
    """ check whether a handle exists"""
    
    if handle == 'n/a' or handle == '' or handle == '""': # return "OK" if the handle is n/a is empty
        result = 'OK'
    else:
        try:
            twitterQuery = 'https://api.twitter.com/1.1/users/show.json?' + 'screen_name=' + handle
            T_response,json_string = client.request(twitterQuery)
            json_string = json.loads(json_string)
            json_string['errors'] #attempt to look for error message
            result =  '---------------------------------Error!'
        except:
            result = 'OK'
    return result



def TwitterCheck():
    """return list of success and failures for Twitter handles list with
    total counts"""
    TwitterMessageList = ['TWITTER TESTING\n\n']
    TWfound = 0
    TWmissing = 0

    TokenStatus, TokenMessage = TestActiveTwitterToken('MichaelCurrin') # check whether token works by testing URL for a controlled page
    TwitterMessageList.append(TokenMessage)

    # continue to test handles if token is valid
    if TokenStatus == 'OK':
        for clientName in TWInputCompetitorHandles:   # look through client names
            str1= clientName 
            TwitterMessageList.append(str1)
            #print str1

            for index in range(len(TWInputCompetitorHandles[clientName])): # look through handles in client
                str2= '    %s' % TWInputCompetitorHandles[clientName][index] # e.g. @AmstelSA
                str3 = TwitterReturnUserExists(TWInputCompetitorHandles[clientName][index]) # e.g. OK or Error
                str4 = str2 + '    ' + str3
                #print (str4)
                TwitterMessageList.append(str4)

                if str3 =='OK':
                    TWfound += 1
                else:
                    TWmissing +=1
    else:
        TWmissing = -1

    TWsummary = '\n%i of %i Twitter handles found\n\n' % (TWfound,(TWfound + TWmissing))
    TwitterMessageList.append(TWsummary)
    try:
        TwitterMessage = '\n'.join(TwitterMessageList)   # convert list to string
        # occasional error. possibly from rate limits.
        #"TypeError: sequence item 1: expected string, list found."
        return TwitterMessage, TWmissing
    except:
        return 'Twitter check could not be completed',TWmissing



#-------CREATE MAIL CONTENT------------------


FacebookEmailMessage,FBEmailmissing = '', 0 # default values which can be overwritten by the next line
FacebookEmailMessage,FBEmailmissing = FacebookCheck() # disable this line to turn FB off and still send a mail

TwitterEmailMessage, TwitterEmailMissing = '', 0 # default values which can be overwritten by the next line
TwitterEmailMessage, TwitterEmailMissing = TwitterCheck() # disable this line to turn FB off and still send a mail

# manually inputted notes

EmailNotes = ('NOTES:\nNone')

# test FB and Twitter and format for a mail
FullMessagePart1 = ('Hello,\n\nPlease find  your Python cronjob testing results below'
                    + '\n\n\n' + EmailNotes
                    + '\n\n\nSummary: '
                    + '\n   '+ str(FBEmailmissing) + ' FB errors'
                    + '\n   '+ str(TwitterEmailMissing) + ' Twitter errors'
                    + '\n\n\n' +  FacebookEmailMessage
                    + '\n\n' +  TwitterEmailMessage
                    )

# record completion time, date and time taken since the script started
CompletedTime = datetime.datetime.now() # current time in hours, minutes, seconds
CompletedDate = datetime.date.today() # current date
ElapsedTime = (CompletedTime - StartTime) # duration in hours, minutes seconds
ElaspedSeconds=int(ElapsedTime.total_seconds()) #duration converted to seconds

# format times and duration for the mail
FullMessagePart2 = ('\n\n-----------------'
                + '\nStart time: ' + str(StartTime)
                + '\nEnd Time: ' + str(CompletedTime)
                + '\nDuration: ' + str(ElapsedTime)
                + '\n-----------------'
                + "\nSent from Python Cron")

# combine test results and time taken
FullMessage = FullMessagePart1 + FullMessagePart2

# define subject of mail with count of errors across platforms. show an error message if one of the tokens fails.
Subject = 'CRON Social handles - %s errors on %s' % (str(FBEmailmissing+TwitterEmailMissing), str(CompletedDate))
if FBEmailmissing == -1 or TwitterEmailMissing == -1:
    Subject = 'CRON Social handles - WARNING - API authentication error!'


#-------SEND MAIL------------------

print ('Subject: ' + Subject)

# send mails to the entire recipients list
for address in addressList: # loop through addresses
    try:
        sendMail(FullMessage,Subject,address) # send mail and display confirmation of recipient address
        
        print ('%s - message delivered') % address
    except:
        print ('%s - ERROR! message could not be delivered') % address

# print contents of mail on screen
if False:
    print ('\n\n')
    print ('\n-----------------\nSubject of mail: \n-----------------')
    print (Subject)
    print ('\n-----------------\nContent of email:\n-----------------')
    print (FullMessage)
    print ('\n-----------------')
    print ('\n')

# print total time taken
print 'Total Script duration up to last mail sent'
print datetime.datetime.now() - StartTime #Duration including time to finishing sending the message
