#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:48:30 2016

@author: michaelcurrin

Convert social media handles to numeric ids

For 
 - Facebook TO BE ADDED
 - Twitter TO BE ADDED
 - Instagram
 
The reasons is that IDs are more stable than handles which can be changed. 
And because Instagram API posts query can accept IDs and not handles.
"""
import csv
import json # read <script> data

from bs4 import BeautifulSoup # process HTML
import requests # get web data

import config_social_handles as config


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
    
    # get user data from JSON 
    # - use [0] as there is only one item
    profile = json_data['entry_data']['ProfilePage'][0]['user']
        
    # extract user details
    out_dict = {}
    out_dict['Platform'] = 'Instagram'
    out_dict['ID'] = profile['id']
    out_dict['Full name'] = profile['full_name']
    out_dict['Handle'] = handle #OR profile['username'] from API
    out_dict['Followers'] = profile['followed_by']['count']
    return out_dict
 
 
def main():
    ### Get data for Instagram users ###
    
    user_data = []
    
    IG_users = config.IG_users
    
    for h in IG_users:
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
  
    ### Write to CSV ###
    out_name = 'out_data.csv'
    
    # Use DictWrite to write out dictionary items instead of tuple rows.
    # The order is determined by fieldsnames.      
    with open(out_name, 'w') as csvfile:
        # header
        fieldnames = ['Platform', 'ID', 'Handle',  'Full name', 'Followers']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
            
        for user in user_data:
            # convert UTF-8 if unicode, otherwise do not convert
            for key, value in user.iteritems():
                if isinstance(value, unicode):
                    encoded_value = value.encode('utf-8')
                    user[key] = encoded_value
            # write
            writer.writerow(user)
            
        print 'Done - %s' % out_name
        
if __name__ == '__main__':
    main()


# Sample output
"""
ERROR: "not-a-handle" is not available

IG user data
------------
Platform:   Instagram
Followers:   394
Handle:   thedrawingroomcafe
ID:   1711102403
Full name:   The Drawing Room

...

"""
