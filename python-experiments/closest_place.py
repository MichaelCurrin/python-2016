#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 21:42:22 2016
@author: michaelcurrin

I created this script based on a question I found on Github here, where I was 
able to provide a solution
http://stackoverflow.com/questions/40452887/navigating-through-a-dictionary-in-python/40454121#40454121

The purpose is to find the location which is nearest to the given location 
but also has the features (e.g. gas) which are required.
The script then prints the details of the closest place including the distance to it.
"""
import math


def findDistance(A, B):
    """
    In 2D space find the distance between two co-ordinates is 
    known as Eucliciean distance.
    Args
        A: tuple or list of x and y co-ordinates 
            e.g. (1,2) e.g. [1,2]
        B: as A.
    Returns
        distance: float. Decimal value for shortest between A and B
    """
    x = (A[0] - B[0])
    y = (A[1] - B[1])
    distance = math.sqrt(x**2 + y**2) # square root

    return distance
    

def GetClosestPlace(places, loc, feature):
    """find shortest distance between current location and each locations 
    but only ones which have the desired feature"""

    # add distance from current location to each location
    for index in range(len(places)):
        
        # only continue if feature exists at place
        if feature in places[index]['features']:

            # calculate
            distance = findDistance(loc,
                                    places[index]['location'])
        else:
            # this is to represent n/a for now as every location needs a distance
            # for this version, so that it will not be chosen
            distance = 1000 
        
         # add calculated distance to existing dictionary for location
        places[index]['distance'] = distance    
        
    # Find shortest distance and return details for that place
    
    allDistances = [x['distance'] for x in places]
    shortestDistance = min(allDistances)
    
    for place in places:
        if place['distance'] == shortestDistance:
            return place

        
placesList = [dict(name='foo',location=(0,3), features=['gas', 'food']),
              dict(name='bar',location=(4,6), features=['food', 'hospital']),
              dict(name='abc',location=(0,9), features=['gas','barber']),
              dict(name='xyz',location=(2,2), features=['food','barber'])
              ]
                        
currentLocation = (5,9)
desiredFeature='food'

closestPlace = GetClosestPlace(placesList, currentLocation, desiredFeature)

print 'Current location: %s' % str(currentLocation)
print 'Desired feature: %s ' % desiredFeature
print
print 'The closest place is...'
print 'Name: %s' % closestPlace['name']
print 'Location %s' % str(closestPlace['location'])
print 'Distance %f' % closestPlace['distance']
# join multiple features in the list with commas
print 'Features: %s' % ', '.join(closestPlace['features'])

"""
OUTPUT

Current location: (5, 9)
Desired feature: food 

The closest place is...
Name: bar
Location (4, 6)
Distance 3.162278
Features: food, hospital
"""
