#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 22:12:36 2016

Author: michaelcurrin
Contact: www.twitter.com/MichaelCurrin; https://github.com/MichaelCurrin

### Background ###

In my area (Cape Town, South Africa), car number plates are typically in the format 'CA 123-456'. In traffic, I sometimes add 
up the digits on the left and subtact the digits on the right, to my maths. The letters at the start ignored.
I observed a number plate which had a net value of zero when following my arithmetic rule. I wondered how many ways there are 
to get a zero using 6 digits. And what this probability based on all subtraction outcomes you can get based on 1,000,000 
combinations of digits. 
I suspected that zero would be common as its in the middle of a range of net values.  Since '000-000','001-001','100-001',
'111-111' and '999-999' are all examples of combinations which yield zero.
While a value like 27 is rare as there is only one way to achieve it ('999-000').
But 26 is more common ('998-000', '989-000', '899-000','999-001', etc.)

### Summary ###

The script calculates the probability of observing a number plate which has a value of 0 when subtracting the sum of the 
last 3 digits from the first 3.

Apply for any number of digits but still only 2 terms for subtraction.
(This could later expanded to more terms if adding or multipling all terms e.g. 123*987*456 e.g. 123+234+345)

Any input is allowed in a list in the form 'XXX-XXX' where X is an integer and there are any number of X values on bother 
sides of the dash (minus sign), but at least one X on each side.


### Sample output ###
Inputted value: 000-000
Net sum: 0
Total unique results for available digits: 55
Probability of observing net sum: (55261 occurences / 1000000 outcomes) = 5.526100 %

Inputted value: 999-000
Net sum: 27
Total unique results for available digits: 55
Probability of observing net sum: (1 occurences / 1000000 outcomes) = 0.000100 %



### Pseudo code ###

input string value of X digits and Y digits
    later, for any number of combination of terms
    later, determine operator

add values of 1st term
add values of 2nd term

subtract them

save result


calculate for all possible combinations of X and Y digits
rather than separate, use total digits e.g. 3 digits and 3 digits is 6 digits and this must be the new input but just split down 
the iddle
creat distinct list of outcomes with count of occurences for each, as a dictionary

lookup result in list

add up counts of outcomes

count ways result could occur / total number of outcomes

convert to percentage


"""


def percentage(part, whole):
    result = 100 * float(part) / float(whole)
    return result


def addDigits(string):
    sum = 0
    for char in string:
        sum += int(char)
    return sum


def subTractTerms(inputString):
    inputList = inputString.split("-")
    netSum = addDigits(inputList[0]) - addDigits(inputList[1])
    return netSum


def getPossibleValues(inputString):
    """Arguments: 
            inputString 
                string
                any number of digits followed by a space and more digits
                e.g. '123-214' 
                e.g. '124124124-12421'
    Result:
        formattedRangeStrings
            list
            
    """

    inputList = inputString.split("-")
    lengths = []  # match the word with its length in a list
    possibilities = (
        []
    )  # match the length with the full range of values possible for that number of digits.
    for items in inputList:  # look through words
        # count the digits in the words and add to list
        lengths.append(len(items))

        # The possibilities value with be 1 higher than the max for the 3 digits
        # e.g. calculate for 3 digits which allows a max value of 10**3 = 1000 values
        # derived as (1 or 001 to 999, as 999 values. plus 1 by including 000. equals 1000 values)
        possibilities.append(10 ** len(items))

    # count the number of possible combinations of X digits and Y digits.
    # this can be done by looking at ABC-DEF as one number e.g. 999-999.
    # There are 1,000,000 possible values. 1 to 1,000,000 as 000-000 through to 999,999.
    # therefore only require 10 to the power of the combined digits total

    total = sum(lengths)  # e.g. 3 + 3 = 6
    maxValue = (
        10 ** total
    )  # e.g. 10**6 = 1,000,000 which is the number of values for '000-000' to '999-999'
    fullRangeInt = range(
        0, maxValue
    )  # list of ints e.g. 0 to 999,999. No leading zeroes are used.

    formattedRangeStrings = []
    for integer in fullRangeInt:
        splitPosition = len(str(integer)) - lengths[1]
        # e.g. 5 (from 123456) - 3 (from 456), equals split at character 2
        # for 5 digits (2...3) and only split at 3rd character for 6 digits (3...3)
        string = "%s-%s" % (
            str(integer)[0:splitPosition],
            str(integer)[splitPosition:],
        )  # e.g. 999-999
        formattedRangeStrings.append(string)

    return formattedRangeStrings


def CalculateProbability(testValue):

    possibleValues = getPossibleValues(testValue)
    # e.g. '999-991', '999-992', '999-993', '999-994', '999-995', '999-996', '999-997', '999-998', '999-999']

    # print possibleValues

    possibleValuesNet = []
    for index in range(len(possibleValues)):
        possibleValuesNet.append(
            subTractTerms(possibleValues[index])
        )  # '100-800' becomes -9

    """for index in range(len(possibleValues)): # TEST
        displayLength = '*'*possibleValuesNet[index] # print ******* to show length
        print possibleValues[index], possibleValuesNet[index], '\t', displayLength"""

    uniquePossibleValues = {}
    for items in possibleValuesNet:
        if (
            items in uniquePossibleValues
        ):  # for result -9, check if it exists and add 1 to count, otherwise set count to 1
            uniquePossibleValues[items] += 1
        else:
            uniquePossibleValues[items] = 1

    # for keys in uniquePossibleValues:    print keys, uniquePossibleValues[keys] # TEST

    NumWaysResultCanOccur = uniquePossibleValues[subTractTerms(testValue)]
    # lookup the number of occurences of input subtraction result from results

    CountAllOutcomes = len(
        uniquePossibleValues.keys()
    )  # count number of keys (unique outcomes)
    TotalAllOutcomes = sum(
        uniquePossibleValues.values()
    )  # count of number outcomes including duplicates
    Probability = percentage(NumWaysResultCanOccur, TotalAllOutcomes)

    # possibleGrouped = dict(zip(possibleValues,possibleValuesNet)) # e.g. 5:3

    print "Inputted value: %s" % testValue
    print "Net sum: %i" % subTractTerms(testValue)
    print "Total unique results for available digits: %i" % CountAllOutcomes
    print "Probability of observing net sum: (%i occurences / %i outcomes) = %f %%" % (
        NumWaysResultCanOccur,
        TotalAllOutcomes,
        Probability,
    )
    print ""


# alternative input: number of X digits and Y digits and outcome e.g. 0.
# although 000-000 is a good simplification
# or #001-000 for value of 1


plates = ["000-000", "999-000", "989-000", "123-456", "0-0", "9-0", "999-00"]
# future development
# inputPlate = raw_input("Enter you value in the form XXX-XXX")

# calculate probability of observing the subtraction result, not the actual plate
for items in plates:
    CalculateProbability(items)

# future development
# generatedPlates = getPossibleValues('000-000') # generate all plates for 6 digits. this can be used as input for the probablity
# calculation and then to find the distribution, but returns a neater method than printing 4 lines each time.
