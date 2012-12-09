#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script written in response to coding puzzle issued
# by Spotify.  Script reads a file with a single line
# that is the Year / Month / Day in any possible order and
# prints the earliest possible expiration date.
# 
# 
# Coding Challenge: http://www.spotify.com/us/jobs/tech/best-before/
#
# Script written by Glen Baker - iepathos@gmail.com

###############################################

import sys
import datetime
import itertools

earliest_date = datetime.date(2000, 01, 01)
latest_date = datetime.date(2999, 12, 31)

def bestbefore(date_str):
    """ This function finds the earliest expiration date between
    the earliest_date and latest_date given an ambiguous date
    string Year / Month / Day in no particular order """
    date_int = map(int, date_str.split('/')) # set items from input string to int
    # For ambiguous dates: sorted ( list of possible year / month / day combinations )
    ambiguous_dates = sorted(itertools.permutations(date_int, 3))
    expiration_date = None
    for date in ambiguous_dates:
        year = date[0] + 2000 if date[0] < 1000 else date[0]
        try:
            possible_date = (str(year), str(date[1]), str(date[2]))
            _possible_date = datetime.date(*[int(x) for x in possible_date])
            if expiration_date is None or _possible_date < expiration_date:
                expiration_date = _possible_date
        except ValueError:
            pass

    if expiration_date is None or expiration_date < earliest_date or expiration_date > latest_date:
        print date_str, 'is illegal'
    else:
        print expiration_date

if __name__ == '__main__':
    # Input is a line 'day / month / year' with no specific order
    for line in sys.stdin:
        bestbefore(line.strip())
