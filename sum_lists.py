#!/usr/bin/env python
# -*- coding: utf-8

def sum_lists(list_a, list_b):
	sums = []
	for x in list_a:
		for y in list_b:
			sums.append(x+y)
	return set(sums)

list_a = [1, 2]
list_b = [3, 4]
print sum_lists(list_a, list_b)
