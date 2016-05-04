#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Created on Thu Apr 28 10:03:59 2016

@author: michaelcurrin

Bash_Search_Install.py
This script defines a short Console function to pass commands to the Mac / Unix terminal.
The command line code used in this script includes retrieving folders in the working directory or a subfolder, which match a condition.
It also allows you to install a number of libraries.

"""

import subprocess

def Console(command): 
    """Take input instruction for console as string. Run it in the terminal. Return the result in output string.

    Arguments:
        command
            string to excecute
            e.g. 'ls'
    """
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True) # split turns string into array
    output = process.communicate()[0]

    return output


def ConsoleSearch(fileExtension, folderName):
    """Search a subfolder and return a list of files of folders which contain the input string.
    
    Arguments: 
        fileExtension
            The string to search for, which could be a part of a filename if it excludes a dot. 
            e.g. '.csv' 
            e.g. '2016'
        folderName
            The name of the subfolder to search within. 
            Leave blank if not required. 
            e.g. 'Inputs' 
            e.g. ''
    """

    if folderName:
        cmd = 'cd %s; ls' % folderName
    else:
        cmd = 'ls'
    string = Console(cmd)  # go to subfolder. Then show a list of files and folders within. The result will be empty if the folder does not exist.
    array = string.split() # convert string result with "\n" delimeter into a list
        
    fileArray = []
    for name in array: # loop through names looking for those containing fileExtension and add to array
        if fileExtension in name.lower():
            fileArray.append(name)
    
    return fileArray  


def ConsoleInstall(libraries):
    """Loop through a list of library names which have been provided as input.
    Attempt to install using Console function.
    Show OK if installing successfully or previous, othterwise show a FAIL message.

    Arguments
        libraries
            list of library names to be installed
            e.g. ['oauth2', 'Flask']
    """
    
    for lib in libraries:
        installCommand = 'pip install %s' % lib
        try:
            Console(installCommand)
            print installCommand + ' ... OK'
        except:
            print installCommand + ' ... FAIL'


if __name__ == '__main__': 
    # run if  Bash_Search_Install.py file is executed directly. ignore if it is imported into another Py file
    
    """ test the Console function with navigating up a level"""
    test = 'ls; pwd; cd ..; pwd' 
    print Console(test)
    print '---'
    
    """ test the Console function with navigating to a subfoler 'Inputs'"""
    test = 'pwd; cd Inputs; pwd; ls' # requires Inputs folder to exist in working directory of current Py file
    print Console(test)
    
    """ test the ConsoleSearch function without subfolder """
    ext = '.py'
    subf = ''
    print ConsoleSearch(ext, subf)
    print '---'    
    
    """ test the Console function in subfolder"""
    ext = '.csv'
    subf = 'Inputs'
    print ConsoleSearch(ext, subf)
    print '---'    
    
    """ test the ConsoleInstallModules function """
    testList = ['oauth2', 'Flask']
    print ConsoleInstall(testList)
    print '---'       
