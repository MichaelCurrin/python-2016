# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:03:59 2016

@author: michaelcurrin


"""

import subprocess

def Console(command): 
    """input instruction for console, run it and save the result in output string."""
    
    try:     
        process = subprocess.Popen(command, stdout=subprocess.PIPE) # problem might be process closes after each cmd
        output = process.communicate()[0]
    except:
        output = "Error"
    
    return output


def SearchForFileType(fileExtension):
    """return an array of filenames which contain fileExtension input (e.g. 'csv'), using Console function. """
    
    string = Console(['ls']) # get the list of files and and folders in the directory of this Py file.
    array = string.split() # convert string with \n signs into array
        
    fileArray = []

    for name in array: # loop through names looking for those containing 'csv' and add to array
        if fileExtension in name.lower():
            fileArray.append(name)
    return fileArray   


def InstallModules():
    """Loop through a list of libraries to install.
    Attempt to install using Console function and show OK/FAIL result."""
    
    modules = ['oauth2']    
    for lib in modules:
        install = 'pip install %s' % lib
        try:
            Console(install) # attempt to install library if not already installed
            print install + ' . . . OK'
        except:
            print install + ' . . . FAIL'
       
       
# test #http://stackoverflow.com/questions/8601312/python-passing-multiple-parameters-for-popen-command
command = ['cd ..', 'pwd'] # cd .. gives an error
process = subprocess.Popen(command, stdout=subprocess.PIPE) # problem might be process closes after each cmd
output = process.communicate()[0]   
print output      
            
            
#print SearchForFileType('.csv') # require full stop otherwise py files containing csv in the name are returned.