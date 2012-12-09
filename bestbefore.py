#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script written in response to coding puzzle issued
# by Spotify.  Script reads a file with a single line
# that is the Year / Month / Day in any possible order and
# prints the earliest possible expiration date.
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
    """ This function finds the earliest expiration date between 2000 and 2999 given a date string Year / Month / Day in no particular order """
    date_int = map(int, date_str.split('/')) # set items from input string to int
    # for ambiguous dates: sorted ( list of possible year / month / day combinations )
    ambiguous_dates = sorted(itertools.permutations(date_int, 3))
    expiration_date = None
    
    for date in ambiguous_dates:
        # year= date[0]
        year = date[0] + 2000 if date[0] < 1000 else date[0]
        try:
            possible_date = datetime.date(year, date[1], date[2]).strftime('%Y-%m-%d')

            if expiration_date is None or possible_date < expiration_date and possible_date >= earliest_date and possible_date <= latest_date:
                expiration_date = possible_date
        except ValueError:
            pass

    if expiration_date is None:
        print date_str, 'is illegal'
    else:
        return expiration_date

if __name__ == '__main__':
    # input is a line 'day / month / year' with no specific order
    # Beyond Requirements: will process multiple lines and dates from a single file
    for line in sys.stdin:
        print bestbefore(line.strip())
