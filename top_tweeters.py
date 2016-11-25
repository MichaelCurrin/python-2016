#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 23:12:33 2016

@author: michaelcurrin

Get the handles of top users on twitter from socialblade.com,
for 4 categories.
Create a sorted list of unique handles across the lists.
Print it.
"""
import requests

# Setup categories and URLs

base_url = 'https://socialblade.com/twitter/top/100/%s'
pages = [dict(name= 'Top Followers', url= base_url % 'followers'),
         dict(name= 'Top Following', url= base_url % 'following'),
         dict(name= 'Most Tweets', url= base_url % 'tweets'),
         dict(name= 'Most Engagements', url = base_url % 'engagements')
         ]

# Query each URL and store HTML RSULT
for i in range(len(pages)):
    pages[i]['handles'] = [] # create empty list in dict
    
    url = pages[i]['url']
    html = requests.get(url).content

    # split by line break, quotation marks and then forwardslash, to 
    # extract 100 user handles from a page
    
    row_split = html.split('\n')
    for row in row_split:
        if 'twitter/user' in row:
            quote_split = row.split('"')[-2]
            slash_split = quote_split.split('/')[3]
            handle = slash_split
            pages[i]['handles'].append(handle)

# set to True to print contents of each list
if False: 
    for item in pages:
        print item['name']
        print '----------'
        for i, h in enumerate(item['handles']):
            print '%i) %s' % (i+1, h)  
        print

            
# Create unique list
unique_handles = []

for item in pages:
    for handle in item['handles']:
        if handle not in unique_handles:
            unique_handles.append(handle)
            

# Sort and print unique list
sorted_handles = sorted(unique_handles)
print 'Top Twitter handles'
for i, h in enumerate(sorted_handles):
    print '%i) %s' % (i+1, h)

# Sample result
"""
Top Twitter handles
1) 2m___m2
2) 2morrowknight
3) 2of__
4) 2thank
5) 5SOS

...
374) xtina
375) yokoono
376) youm7
377) yvesjean
378) zaynmalik
"""
