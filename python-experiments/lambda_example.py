# -*- coding: utf-8 -*-
""" flatten a 2 dimensional list into a 1 dimension list
by joining column items in a row into one item as single comma-separated string

This is useful for preparing data for a CSV writer function which requires a 1-dimensional list of rows with no columns
Alternatively, the join functional can be moved into the CSV writer so that the function can accept 2 dimensional lists

"""

list = [("A", "B", "C"), ("34", "32647", "43"), ("4556", "35235", "23623")]


str = map(lambda x: ",".join(x), list)

print str
"""
#output
['A,B,C',
'34,32647,43', 
'4556,35235,23623']
"""
