# -*- coding: utf-8 -*-
"""
Created on 11 Dec 2016

This script is for working with unix timestamps and converting them
to human-readable values.

I've since found that datetime and time packages has this kind of conversion for readability already builtin.

@author: michaelcurrin

"""
import datetime
import time


def UnixToDHMS(duration):
    """
    Convert duration (in unix_timestamp seconds) to days, hours, minutes and 
        seconds.

    Args
        duration: <type 'int'> OR <type 'str'> Duration in seconds. 
            If given as a string, convert to integer.
    Returns
        d: days [0+]
        h: hours [0-23]
        m: minute [0-59]
        s: seconds [0-59]
    """
    duration = int(duration)
    d = duration / (24 * 60 * 60)
    h = duration / (60 * 60) % 24
    m = duration / 60 % 60
    s = duration % 60
    return d, h, m, s


def MyTime(unix_time, hours_diff=0):
    """
    Change unix timestamp in seconds into datetime format, with optional
    time difference hours specified.

    Usecase: receive timestamp from API and return as datetime object
        which has properties 
            year, month, day, hour, minute, second

    Args
        unix_time: unix timestamp in seconds
        hours_diff: <type 'int'> e.g. -2, or 6
            numbers of hours to add or subtract.
    Returns
        out_time: datetime object.
            Shows in format '2016-12-11 15:40:00' if printed
    """
    unix_time_diff = hours_diff * 60 * 60  # hours * min * seconds
    in_time = unix_time + unix_time_diff
    out_time = datetime.datetime.fromtimestamp(in_time)
    return out_time


def MyDuration(duration, initial_time=None):
    """
    Usecase:
        a timestamp is provided as when an access token expires,
         then add it to the current time, then showing it as a human-readable 
         future time.
         Alternatively specify a *initial_time* as manual now value.
    
    Args
        duration: <type 'int'> OR <type 'str'> Duration in seconds. 
            If given as a string, convert to int.
        initial_time: <type 'int'> OR <type 'str'> Time to start differenc
            calculation from. If given as a string, convert to int.
            If not set, use current time.
    Returns
        out_time: what time will it be after number seconds in have elapsed.
            Shows in format '2016-12-11 15:40:00' if printed.
    """
    duration = int(duration)

    if initial_time:
        initial_time = int(initial_time)
    else:
        initial_time = time.time()  # use current time

    in_time = initial_time + duration  # add duration to start time
    out_time = datetime.datetime.fromtimestamp(in_time)

    return out_time


def Test():
    print "### First test ###"
    print

    now = datetime.datetime.now()
    print "Now: %s" % str(now)
    print

    initial_time = 1481463600
    duration = 88075
    x = initial_time + duration
    # print x

    d = UnixToDHMS(duration)
    print "Duration:"
    print " - %i seconds" % duration
    print " - %id %ih %im %is" % d
    print

    t = MyDuration(duration)
    print "Expected time will be: %s" % str(t)
    print

    i = MyTime(initial_time)
    u = MyDuration(duration, initial_time)
    print "Or starting from  %s, it will be: %s" % (str(i), str(u))

    print
    print "### Second test ###"
    print

    print "Hours min sec VS original unix seconds"
    test_seconds = [
        1,  # 1 second
        60,  # 1 minute
        60 * 60,  # 1 hour
        60 * 60 * 2,  # 2 hours
        60 * 60 * 23 + 1,  # 23 hours and 1 second
        60 * 60 * 48,  # 2 days
        1234678,
    ]
    for sec in test_seconds:
        d, h, m, s = UnixToDHMS(sec)

        print "%id %ih %im %is -- %s" % (d, h, m, s, sec)
    print

    print "### Third test ###"
    print
    d_format = "%id %ih %im %is"

    # separate as 1 sec, 2 min, 3 min, 4 days
    d = 1 + 2 * 60 + 3 * 60 * 60 + 4 * 24 * 60 * 60
    print d_format % UnixToDHMS(d)

    d = 61 + 2 * 60 + 25 * 60 * 60 + 0 * 24 * 60 * 60
    print d_format % UnixToDHMS(d)

    d = 87384
    print d_format % UnixToDHMS(d)

    d = 5109691
    print d_format % UnixToDHMS(d)


if __name__ == "__main__":
    Test()
