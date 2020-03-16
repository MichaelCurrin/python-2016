# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 12:48:15 2016
Updated 17 Oct.

@author: @michaelcurrin on Github and Twitter.

This script provides a method for a splitting a list of objects into groupings 
of a maximum size.
The application in mind is that the Twitter API allows you to fetch 100 tweet 
ids at a time in the lookup.json query.
(see https://dev.twitter.com/rest/reference/get/statuses/lookup)

Therefore, given a starting list of 203 tweet ids which you need the data for,
you need 3 URLs to cover 1-100, 101-200 and 201-203.
"""


def SplitListByGrouping(list, x):
    """
    Receive a list of items.
    If the length is longer than x, then split the list into several lists,
    each with a maximum of x elements.
    This is then returned as a 2D array.
       
    Args
        list: list of items in any format or mixed. 
              e.g. ['ABC', 23590.34, 23]
              If a single string is inputted, then the string is split
                  e.g. 'a235235' -> ['a23', '523', '5']
        x:  maximum length to be allowed for any single list. 
            e.g. 100
    Returns:
        outputList: list of items, where each item is a list of maximum 
                    length x.
    """
    outputList = []
    index = 0

    while index < len(list):
        item = list[index : (index + x)]
        outputList.append(item)
        index += x
    return outputList


if __name__ == "__main__":

    # use the function defined above for output test for ListToSplit list.

    print "function version"
    print "================"

    # initial list with 11 items of mixed types
    ListToSplit = [
        "a235235",
        "b",
        "c",
        "d36346",
        23590.3,
        "4574f",
        "g",
        2523,
        "i",
        "j",
        "k",
    ]

    # this is the maximum number of items in each sublist
    grouping = 3  #

    result = SplitListByGrouping(ListToSplit, grouping)

    for item in result:
        print item
    print

    #######

    # Show the  logic used to achieve the function,
    # using first a version with manually specified indices
    # then an auto version which will work with any value of grouping

    # note: it does not matter if the end index is greater than the length of
    # the list
    # e.g. list[0:100]
    #       ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

    print "manual version"
    print "============"

    list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]  # 11 items
    grouping = 3

    row1 = list[0:3]
    row2 = list[3:6]
    row3 = list[6:9]
    row4 = list[9:]

    outputManual = row1, row2, row3, row4

    print "result"
    for item in outputManual:
        print item
    print

    print "auto version"
    print "============"

    list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]  # 11 items
    grouping = 3

    outputList = []
    index = 0
    while index < len(list):
        print index, index + grouping
        item = list[index : (index + grouping)]
        print item

        # note: use  outputList+= [item] or outputList.append(item)
        # since outputList+= item  will just add individual elements to the big list.

        outputList.append(item)
        index += grouping

    print

    print "result"
    for item in outputList:
        print item
