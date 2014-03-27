#!/usr/bin/env python
# -*- coding: utf-8 -*-

def print_ascii_triangle(height):
	left_spacer = ''
	for x in range(height):
		left_spacer += ' '
	middle_spacer = ''
	for x in range(height):
		if x == height-1:
			# print the bottom of the triangle, just a line of underscores
			triangle_bottom = ''
			for space in range(len(middle_spacer)):
				triangle_bottom += '_'
			print ' /' + triangle_bottom + '\\'
		else:
			print left_spacer[x:] + '/' + middle_spacer + '\\'
		middle_spacer += '  '

print_ascii_triangle(3)