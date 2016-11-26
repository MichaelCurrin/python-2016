#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:48:30 2016

@author: michaelcurrin

Convert social media handle to numeric id.

For 
 - Facebook TO BE ADDED
 - Twitter TO BE ADDED
 - Instagram
 
Since IDs are more stable than handles which can be changed. And because
Instagram API posts query can accept IDs and not handles.
"""
import requests # get web data
from bs4 import BeautifulSoup # process HTML
import json # read <script> data

def GetInstagramUserData(handle):
    """
    Load the HTML for a user's profile on www.instagram.com.
    Read fields like user's numeric id from the profile HTML.
    Args
        handle: <type 'str'> Name of Instagram user. If it contains '@'
            then this will be remove.
    Returns
        out_dict: <type 'dict'> Dictionary of user fields and values.
    """
    handle = handle.replace('@','')
    base = 'http://instagram.com/%s/'
    url = base % handle
    
    # access webpage and convert to soup
    req  = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, 'lxml')
    
    # search for scripts
    for script in soup.find_all(u'script', type=u'text/javascript'): 
        text = script.text
        # break when desired script is reached
        if 'ProfilePage' in text:
            break
        
    # extract user profile from script and convert to JSON
    json_start = text.find('{')
    json_end = text.find(';')
    json_string = text[json_start:json_end]
    json_data = json.loads(json_string)
    
    # get user data from JSON (use 0 as there is only one item)
    profile = json_data['entry_data']['ProfilePage'][0]['user']
        
    # extract user details
    out_dict = {}
    out_dict['ID'] = profile['id']
    out_dict['Full name'] = profile['full_name']
    out_dict['Handle'] = handle #OR profile['username']
    out_dict['Followers'] = profile['followed_by']['count']
    return out_dict
 
def Main():
    
    handles = ['johnniewalkersa', 'thedrawingroomcafe', '@michaelcurrin', 
               'not-a-handle']

    user_data = []

    for h in handles:
        try:
            IG_user_data = GetInstagramUserData(h)
        except ValueError:
            IG_user_data = {'Handle':h,
                            'ID':'NOT AVAILABLE'}
            print 'ERROR: "%s" is not available' % h
            print
        user_data.append(IG_user_data) 
    
    print 'IG user data'
    print '------------'
    for u in user_data:
        # Print dictionary
        for k, v in u.iteritems():
            print '%s:   %s' % (k, v)
        print
        
if __name__ == '__main__':
    Main()
    
# to be completed:
#   Twitter
#   Instagram
#   write to CSV

# Sample output
"""
ERROR: "not-a-handle" is not available

IG user data
------------
Followers:   767
Handle:   johnniewalkersa
ID:   524623917
Full name:   Johnnie Walker SA

Followers:   392
Handle:   thedrawingroomcafe
ID:   1711102403
Full name:   The Drawing Room

Followers:   262
Handle:   michaelcurrin
ID:   751590118
Full name:   Michael Ashley Currin

Handle:   not-a-handle
ID:   NOT AVAILABLE
"""
