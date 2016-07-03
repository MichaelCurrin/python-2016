#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Place this file in the same directory as Bash_Search_Install.py and run this 
file, as example of importing and excecuting the functions.
"""

from Bash_Search_Install import *
print Console('pwd') # print directory of this Py script
print ''
print Console('ls') # print list of files in working directory
print ''
print ConsoleSearch('.py') # search for py files
print ''
print ConsoleInstall(['oauth2']) # attempt to install a library
print ''
print Console('pip list') # list of currently installed packages


# Example output you can expect
"""
/Users/michaelcurrin/Google Drive/0 Local/Documents (GD)/Programming/Python/My projects/Social WIP


Bash_Search_Install.py
Bash_Search_Install.pyc
FacebookSearch.py
FacebookSearch.pyc
Inputs
SocialMediaMain 001.py
SocialMediaMain 002.py
SocialMediaMain 003.py
SocialMediaMain 004.py
SocialMediaMain_005.py
api-to-sql-test.py
prettytable.py
prettytable.pyc
readCSV_006 copy.py
test_Bash.py


['Bash_Search_Install.py', 'Bash_Search_Install.pyc', 'FacebookSearch.py', 'FacebookSearch.pyc', 'SocialMediaMain 001.py', 'SocialMediaMain 002.py', 'SocialMediaMain 003.py', 'SocialMediaMain 004.py', 'SocialMediaMain_005.py', 'api-to-sql-test.py', 'prettytable.py', 'prettytable.pyc', 'readCSV_006 copy.py', 'test_Bash.py']

['pip install oauth2 ... OK']


abstract-rendering (0.5.1)
alabaster (0.7.7)
appnope (0.1.0)
appscript (1.0.1)
argcomplete (0.8.9)
astropy (1.0.3)
Babel (2.3.3)
backports-abc (0.4)
backports.shutil-get-terminal-size (1.0.0)
backports.ssl-match-hostname (3.4.0.2)
bcolz (0.9.0)
...

"""