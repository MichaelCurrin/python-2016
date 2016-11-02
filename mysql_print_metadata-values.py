#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:10:03 2016

@author: michaelcurrin


Open a connection to a database
Print the tables and column data metadata
Print the actual values for the some tables, for a defined table limit and row count.
Close the database.

"""

import MySQLdb # library to connect to MySQL
import sql_config # file for authorising login

def GetRows (statement):
    """
    Receive a query  and return sthe reuslts from the database.
    Args
        statement: string. e.g. 'SELECT * FROM tablenameXYZ'
    Returns
        output: list of row data from query results
    """

    cur.execute(statement)
    output = []
    for row in cur.fetchall():
        output.append(row)
        
    return output
 
def PrintTable(selectedTable, limit):

    print 'ACTUAL VALUES FOR %s'% selectedTable
    print ''
    
    # Print header
    print tablesColumnsDict[selectedTable]
    
    # Print row values
    #limit = 100
    query = 'SELECT * FROM %s LIMIT %i;' % (selectedTable, limit)
    for rows in  GetRows(query):
        print rows
    # e.g. (808L, datetime.datetime(2015, 11, 1, 0, 0), 'Week 4', 'WinStuff', 
    #      Actual', 600L, 5L, Decimal('0.0373'), 3000L, 134L, 3L)
    print '\n'   
    
def Main():

    dbCredentials = sql_config.dbCredentials

    db = MySQLdb.connect(host= dbCredentials['host'],
                         user= dbCredentials['user'],
                         passwd= dbCredentials['passwd'],
                         db= dbCredentials['dbName'])              
    cur = db.cursor()

    # list of SQL queries to execute
    metadata_scripts = [ # get list tables and row counts for selected DB
            """SELECT 
    		TABLE_NAME
            ,TABLE_TYPE
            ,TABLE_ROWS
            FROM information_schema.tables
            WHERE TABLE_SCHEMA = '%s';
            """ % dbCredentials['dbName'],
            
            # get list of tables and their columns for selected DB
            """SELECT  
    		TABLE_NAME
            ,COLUMN_NAME
            ,COLUMN_DEFAULT
            ,IS_NULLABLE
            ,DATA_TYPE
            ,COLUMN_TYPE
            FROM information_schema.columns
            WHERE TABLE_SCHEMA = '%s';
            """ % dbCredentials['dbName']
            ]


    # Fill a list of tables and views in current DB

    tableNames = [] 
    tableNameData= GetRows(metadata_scripts[0])
    for rows in tableNameData:
        # get value in first column (table name)
        tableNames.append(rows[0])  

    if True: # TEST
        print 'TABLE NAMES\n'
        for items in tableNames: 
            print items
        print ''


    # Fill a dictionary containing table name as key as column name as values in a list

    tablesColumnsDict = {}
    tablesColumnsData= GetRows(metadata_scripts[1])
    for rows in tablesColumnsData:
        
        # get value in first column (table name)
        col1,col2 = rows[0:2]
        
        # create empty list for table if it does not exist
        if col1 not in tablesColumnsDict.keys():
            tablesColumnsDict[col1] = []
        # set TABLE_NAME as key and COLUMN_NAME as value
        tablesColumnsDict[col1].append(col2)


    if True: # TEST
        print 'TABLES AND COLUMNS\n'
        for keys in sorted(tablesColumnsDict.keys()):
            print keys    
            for values in tablesColumnsDict[keys]:
                print '\t%s' % values 
            print ''
        print ''
        
    if True: # TEST
        # This works to call global variable tablesColumnsDict 
        # without adding to each method 
                
        # Print X rows for first Y tables
        maxTables = 2
        rowLimit = 5
        count = 0
        for tables in sorted(tablesColumnsDict.keys()):
            if count == maxTables:
                break
            else:
                PrintTable(tables,rowLimit)
                count += 1
        
    # close the database connection
    db.close()


if __name__ == '__main__':
    Main()
