#!/usr/bin/env python3

#Author: Zhiwei Luo

class Cell:
	x = -1
	y = -1
	hasTopWall = False
	hasDownWall = False
	hasLeftWall = False
	hasRightWall = False

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def setTopAsWall(self):
		self.hasTopWall = True

	def setLeftAsWall(self):
		self.hasLeftWall = True

	def setRightAsWall(self):
		self.hasRightWall = True

	def setDownAsWall(self):
		self.hasDownWall = True

	def setAllAsNoWall(self):
		self.hasTopWall = False
		self.hasDownWall = False
		self.hasLeftWall = False
		self.hasRightWall = False

	# For Testing
	def getWhichIsWall(self):
		whichIsWall = '[Wall]'
		if self.hasTopWall:
			whichIsWall += 'Top '

		if self.hasDownWall:
			whichIsWall += 'Down '

		if self.hasRightWall:
			whichIsWall += 'Right '

		if self.hasLeftWall:
			whichIsWall += 'Left '

		return whichIsWall