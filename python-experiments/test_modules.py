#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Michael Currin

This script is designed to test installations of downloaded modules.
This can be double-clicked if named test_modules.command
However, this means that the environment can not be set.
Therefore it is better to run this from the console after choosing the environment.
Make this executable:
	$ chmod +x test_modules.py
Execute with python
	$ test_modules.py


Note that "python" can be omitted from 
	$ python test_modules.py
 since the python shebang has been included in this script.
"""
print "starting imports..."
print

print '#### Basic ####'
try:
	import httplib2
	print 'OKAY - httplib2'
except ImportError as e:
	print 'ERROR - %s' % e

try:
	import oauth2
	print 'OKAY - oauth2'
except ImportError as e:
	print 'ERROR - %s' % e

print
print '#### Facebook Ads ####'
try:
	import facebookads
	print 'OKAY'
except ImportError as e:
	print 'ERROR - %s' % e

print
print '#### Google Analytics ####'
try:
	from apiclient.discovery import build
	print 'OKAY - apiclient'
except ImportError as e:
	print 'ERROR - %s' % e

try:
	from oauth2client.service_account import ServiceAccountCredentials
	print 'OKAY - oauth2client'
except ImportError as e:
	print 'ERROR - %s' % e

print
print '#### Google Sheets ####'
try:
	from apiclient import discovery
	from oauth2client import client
	from oauth2client import tools
	from oauth2client.file import Storage
	print 'OKAY'
except ImportError as e:
	print 'ERROR - %s' % e

print
print '#### Google Ads ####'
try:
	import googleads
	print 'OKAY'
except ImportError as e:
	print 'ERROR - %s' % e

print
print "ended"
