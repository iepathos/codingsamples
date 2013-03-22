#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script written in response to Convertro
# coding interview question.  Using only list comprehension, 
# read a set of XML files each with a person data structure:
# firstName, lastName, address, and phone number.  List the
# first names of the people who share last names, sorted 
# alphabetically by their first name.
# Written by Glen Baker - iepathos@gmail.com
""" person.xml
<person>
	<firstName>Glen</firstName>
	<lastName>Baker</lastName>
	<address></address>
	<phoneNumber>559.246.8891</phoneNumber>
</person>
"""
# This script assumes xml files are in the directory with the script.
import os, glob
import collections
import xml.etree.ElementTree as ET
xml_set = [f for f in glob.glob('*.xml')]
lastNames = [ET.parse(f).findtext('lastName') for f in xml_set]
firstNames = [ET.parse(f).findtext('firstName') for f in xml_set]
common_lastNames = [lastName for lastName, count in collections.Counter(lastNames).items() if count > 1]
indexes = [item for item in range(len(lastNames)) if lastNames[item] in common_lastNames]
solution = [firstNames[index] for index in indexes]
print sorted(solution)