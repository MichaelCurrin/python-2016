#!/bin/sh

# I use Python 2.7 and Anaconda as my basic environment.
# I've intalled a libraries to get me access to certain social and Google APIs and to MySQL.
# I'd advise you to install these one at a time and also in a cloned environment. I've had an issue before
# installing gdata library (not shown here) - it caused issues with another library so I had to start over
# with a new installed environment.

############################################################################################################
# PIP
############################################################################################################

# Install PIP
# which is a recursive acronym which stands for Pip Install Programs
# and sudo is super user do, for higher access rights of your user.
# You can then use pip to install other libraries.

sudo easy_install pip

############################################################################################################
Google Analytics
############################################################################################################

# install Google Analytics API and a few related libraries
# (alternatively download  with your browser and install that)

pip install --upgrade google-api-python-client

############################################################################################################
# OAuth
############################################################################################################

# install OAuth2
# The oauth2 part is needed for Twitter API
# The oauth2client part is needed for Google Sheets API

pip install oauth2

############################################################################################################
# MySQLdb
############################################################################################################


# I get an error on the recommend method of $ pip install MySQL-python
#
# - Could not find a version that satisfies the requirement MySQLdb (from versions: ) No matching distribution
#    found for MySQLdb
# - Command "python setup.py egg_info" failed with error code 1 in 
#    /private/var/folders/n1/szptw8v90g17xgl59h2mj1jm0000gn/T/pip-build-yuUPhe/MySQL-python/

# After much searching I found this alternative:

# if already installed can be read at $ code-select
xcode-select --install

# this affects the current bash session only and it not permanent
export PATH=$PATH:/usr/local/mysql/bin/

# this gives error if path is not set above.
# - EnvironmentError: mysql_config not found
sudo pip install MySQL-python

############################################################################################################
# Facebook Ads
############################################################################################################

pip install facebookads


############################################################################################################
# Google Adwords
############################################################################################################

sudo pip install googleads
