#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on Thu Apr 28 10:03:59 2016

@author: michaelcurrin

This script defines functions used to pass commands to the Mac or Unix
 terminal, as comand line or bash code. 
The capabilities are explained within each function.

To see how to run this script in other scripts, 
    place test_Bash.py and Bash_Search_Install.py in the same directory. 
    Run testConsole script.

"""

import subprocess

def Console(command): 
    """Take input instruction for console as string. 
    Run it in the terminal. 
    Return the result in output string.
    
    The online Python documentation on the subprocess library includes notes 
    and cautions on use of shell=True versus shell=False.

    Arguments:
        command
            string of commands to excecute, separated by a semi-colon
            e.g. 'ls'
            e.g. 'pwd'
            e.g. 'ls; pwd; cd ..; pwd' 
	Returns:
		output
		response from the terminal
    """
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]

    return output


def ConsoleSearch(searchTerm = '', folderName =''):
    """
    Use the console to return a list of files and folders, within an 
    optionally defined subdirectory. 
    Otherwise use the current working directory of the script which is running.

    Search for files and folders which contain the inputted search text, or 
    leave input blank to show all results.

    
    Arguments: 
        searchTerm
            The string to search for in the file name and/or extension
            e.g. ''
            e.g. '.csv' 
            e.g. '2016'
            e.g. ' 2016.xls'
        folderName
            The exact name of the subfolder directory to search within. 
            e.g. 'Inputs/' 
            
            Use a forward slash as below for tree structure.
            e.g. 'Projects/Completed/'
            
            This is optional. You can set as empty string or omit it.
            e.g. ''
            
            If the location is not valid, the working directory will be used.
            
            Use single quotes within the name, to ensure the terminal 
            accepts the folder name with its spaces .
            e.g. "'July 2016'/"
            
    Returns
    	fileArray
    		list
    		response from the terminal
    		names of file or foldernames which match the search parameters
    """

    # check if a subfolder is defined and navigate to it.
    # show a list of files and folders at the location'. 
    if folderName:
        cmd = 'cd %s; ls' % folderName
    else:
        cmd = 'ls'
    string = Console(cmd)  
    # convert string result with "\n" delimeter into a list
    array = string.split('\n') 
    
    # check if a search term filter needs to be applied
    if searchTerm:
        fileArray = []
        # loop through names looking for those containing searchTerm and 
        # add to array
        for name in array: 
            if searchTerm in name.lower():
	            if folderName: # add path to filenames
	                fileArray.append('%s/%s' % (folderName, name))
                     # e.g. 'Inputs/authentication.csv'
	            else:
	                fileArray.append(name) 
                     # e.g. 'authentication.csv'
    else:
		fileArray = array
                
    return fileArray  


def ConsoleInstall(libraries):
    """
    Loop through a list of library names which have been provided as input.
    Attempt to install them by passing 'pip install' and the library name
    to the Console function defined in this script
    Show the outcome as OK (installed or already exists) or FAIL.

    Arguments:
        libraries
            list 
            library names to be installed
            e.g. ['oauth2', 'Flask']
    Returns:
        	installResultList
             list
             response from the terminal as libraries attempted to be installed, 
             along with the outcome for each.
             The list should contain at least once library name.
    """
    
    installResultList = []
    for lib in libraries:
        installCommand = 'pip install %s' % lib
        try:
            Console(installCommand)
            outcome = 'OK'            
        except:
            outcome = 'FAIL'               
        installResultList.append('%s ... %s' % (installCommand, outcome))     
    return installResultList


if __name__ == '__main__': 
    # run code below as a test if Bash_Search_Install.py file is executed 
    # directly. ignore if it is imported into another Py file
    
    print """1) test the Console function by navigating up a level"""
    cmd = 'ls; pwd; cd ..; pwd' 
    print 'Command: %s' % cmd
    print Console(cmd)
    print '\n'   
    
    print """2) test the Console function by navigating down to a subfolder called 'Inputs'"""
    # requires Inputs folder to exist in working directory of current Py file
    cmd = 'pwd; cd Inputs; pwd; ls' 
    print 'Command: %s' % cmd
    print Console(cmd)
    print '\n'   
    
    print """3) test the ConsoleSearch function, without args, to show all"""
    print ConsoleSearch()
    print '\n'   
    
    print """4) test the ConsoleSearch function, without a define subfolder"""
    term = '.py'
    print 'Term: %s' % term
    print ConsoleSearch(searchTerm=term)
    print '\n'    
    
    print """5) test the Console function in subfolder. Search for '.csv'"""
    term = '.csv'
    subf = 'Inputs'
    print 'Search for %s in %s' % (term, subf)
    print ConsoleSearch(searchTerm=term, folderName=subf)
    print '\n'    
    
    print """6) test the ConsoleInstallModules function with 2 library names"""
    testList = ['oauth2', 'Flask']
    print ConsoleInstall(testList)
    print '\n'      

    print """7) Print a list of installed packages"""
    cmd = 'pip list'    
    print Console(cmd)
    print '\n'     
