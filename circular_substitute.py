#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
alphabet = string.ascii_lowercase

def circular_substitute(string_s, shift_n):
	results = ''
	for letter in string_s:
		# not doing anything with empty spaces for now, simple substitution
		if letter == ' ':
			results += ' '
		else:
			alphabet_index = alphabet.index(letter)
			if alphabet_index + shift_n > len(alphabet):
				results += alphabet[(alphabet_index+shift_n)- len(alphabet)]
			else:
				results += alphabet[alphabet_index+shift_n]
	return results

example_string = 'some fancy test stringz'
print circular_substitute(example_string, 5)