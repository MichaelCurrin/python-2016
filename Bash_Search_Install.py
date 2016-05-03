# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:03:59 2016

@author: michaelcurrin

This script defines a short Console function to pass commands to the Mac / Unix terminal.
The command line code used in this script includes retrieving folders in the working directory or a subfolder, which match a condition.
It also allows you to install a number of libraries.

"""

import subprocess

def Console(command): 
    """take input instruction for console (string), run it in the terminal and save the result in output string."""
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True) # split turns string into array
    output = process.communicate()[0]

    return output
    
def SearchFor(fileExtension):
    """take the input string (e.g. 'csv') and return a list of files and folders which contain it."""
    
    string = Console('ls') # get the list of files and and folders, in the directory of this Py file
    array = string.split() # convert string result with "\n" delimeter into a list
        
    fileArray = []
    for name in array: # loop through names, looking for those containing fileExtension, then add to array
        if fileExtension in name.lower():
            fileArray.append(name)
    
    return fileArray   

def SearchInFolder(fileExtension, folderName):
    """take the fileExtension input string (e.g. 'csv') and search a subfolder (e.g. 'Inputs') and return a list of files and folders which contain the string."""

    string = Console('cd %s; ls' % folderName)  # go to subfolder. Then show a list of files and folders within. The result will be empty if the folder does not exist.
    array = string.split() # convert string result with "\n" delimeter into a list
        
    fileArray = []
    for name in array: # loop through names looking for those containing fileExtension and add to array
        if fileExtension in name.lower():
            fileArray.append(name)
    
    return fileArray  


def InstallModules(modules):
    """Loop through a list of libraries inputted.
    Attempt to install using Console function.
    Show OK if installing successfully or previous, othterwise show a FAIL message."""
    
    for lib in modules:
        install = 'pip install %s' % lib
        try:
            Console(install)
            print install + ' ... OK'
        except:
            print install + ' ... FAIL'


""" test the Console function """
cmd = 'ls; pwd; cd ..; pwd' 
#print Console(cmd)

""" test the Console function """
cmd = 'pwd; cd Inputs; pwd; ls' # requires Inputs folder to exist in working directory of current Py file
#print Console(cmd)

""" test the SearchFor function """
ext = '.csv'
#print SearchFor(ext)

""" test the SearchInFolder function """
ext = '.csv'
subf = 'Inputs'
#print SearchInFolder(ext, subf)

""" test the InstallModules function """
modules = ['oauth2', 'Flask']
#print InstallModules(modules)
