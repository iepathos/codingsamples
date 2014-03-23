#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""	
	Creates a 2d matrix that can print out in spiral order.
	Created as a response to a coding test.

	Written by Glen Baker - iepathos@gmail.com

	Example usage from a Python shell:
	>>> from matrix import Matrix
	>>> matrix = Matrix('1 2 3 4 5 6 7 8 9', 3)
	>>> matrix.spiral
	>>> '1 2 3 6 9 8 7 4 5'

	>>> matrix2 = Matrix('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16', 4)
	>>> matrix2.spiral
	>>> '1 2 3 4 8 12 16 15 14 13 9 5 6 7 11 10'

"""

class Matrix(object):
	"""
		Matrix objects is built given a string of spaced numbers and the number of columns.
	"""
	numbers = []
	matrix = []
	rows = 0 # total number of rows
	columns = 0 # total number of columns
	spiral = '' # numbers output in clockwise spiral order

	def __init__(self, numbers, columns):
		"""Expects spaced numbers string and the matrix width."""
		self.numbers = str(numbers).strip().split(' ')
		self.columns = int(columns)
		self.rows = len(self.numbers)/self.columns

		matrix = [[0 for x in xrange(self.columns)] for x in xrange(self.rows)]
		# put the numbers to the matrix
		k = 0
		for i in range(self.rows):
			for j in range(self.columns):
				matrix[i][j] = self.numbers[k]
				k += 1
		self.matrix = matrix
		self.spiral = self.spiral()

	def spiral(self):
		"""Print out matrix in spiral order, clockwise."""
		spiral_order = ''
		top_row = 0 # current top row index
		left_column = 0 # current first column index
		bottom_row = self.rows # ending row index
		right_column = self.columns # ending column index
		while top_row < bottom_row and left_column < right_column:
			# across the top row
			i = left_column
			while i < right_column:
				#print matrix[k][i]
				spiral_order += ' ' + self.matrix[top_row][i]
				i += 1
			top_row += 1
			# down the last column
			i = top_row # we set the iterator here to top row value
			while i < bottom_row:
				#print matrix[i][n-1]
				spiral_order += ' ' + self.matrix[i][right_column-1]
				i += 1
			right_column -= 1
			# across the last row
			if top_row < bottom_row:
				i = right_column - 1
				while i >= left_column:
					#print matrix[m-1][i]
					spiral_order += ' ' + self.matrix[bottom_row-1][i]
					i -= 1
				bottom_row -= 1
			# back up the first
			if left_column < right_column:
				i = bottom_row -1
				while i >= top_row:
					#print matrix[i][l]
					spiral_order += ' ' + self.matrix[i][left_column]
					i -= 1
				left_column += 1
		return spiral_order.strip()