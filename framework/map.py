#!/usr/bin/env python3

"""
	*map* module contains *class* **Cell** and **Map**.
"""

#Author: Zhiwei Luo

class Cell:
	x = -1
	y = -1
	hasUpWall = False
	hasDownWall = False
	hasLeftWall = False
	hasRightWall = False

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def setUpAsWall(self):
		self.hasUpWall = True

	def setLeftAsWall(self):
		self.hasLeftWall = True

	def setRightAsWall(self):
		self.hasRightWall = True

	def setDownAsWall(self):
		self.hasDownWall = True

	def setAllAsNoWall(self):
		self.hasUpWall = False
		self.hasDownWall = False
		self.hasLeftWall = False
		self.hasRightWall = False

	# For Testing
	def getWhichIsWall(self):
		whichIsWall = '[x=' + str(self.x) + ' y=' + str(self.y) + ']'
		if self.hasUpWall:
			whichIsWall += 'Up '

		if self.hasDownWall:
			whichIsWall += 'Down '

		if self.hasRightWall:
			whichIsWall += 'Right '

		if self.hasLeftWall:
			whichIsWall += 'Left '

		return whichIsWall

class Map:
	"""
	The Map class represents a maze map. The single instance of the Map is stored in a micromouse. 
	You can access the local map of a micromouse by ``mouse.mazeMap``.

	It maintains:
		* the size of the map: *height*, *width*
		* the cells of the map: The cells are represented by a 2-D list array.
	"""
	height = 0
	width = 0
	cells = None

	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.cells = [[Cell(j, i) for i in range(width)] for j in range(height)]

	def getCell(self, x, y):
		"""
		Get the cell instance by given coordinates *x* and *y*. 

		You may need to first call this function before you update or query a map.
		"""
		if x >= 0 and y >= 0 and x < self.width and y < self.height:
			return self.cells[x][y]
		else:
			return None

	def getCellUpWall(self, cell):
		"""
		Return True if there is a wall above the given cell, otherwise return False.

		You may use this function by ``getCellUpWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		return cell.hasUpWall

	def getCellDownWall(self, cell):
		"""
		Return True if there is a wall below the given cell, otherwise return False.

		You may use this function by ``getCellDownWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		return cell.hasDownWall

	def getCellLeftWall(self, cell):
		"""
		Return True if there is a wall on the left side of the given cell, otherwise return False.

		You may use this function by ``getCellLeftWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		return cell.hasLeftWall

	def getCellRightWall(self, cell):
		"""
		Return True if there is a wall on the right side of given cell, otherwise return False.

		You may use this function by ``getCellRightWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		return cell.hasRightWall

	def getRightCell(self, cell):
		return self.getCell(cell.x + 1, cell.y)

	def getLeftCell(self, cell):
		return self.getCell(cell.x - 1, cell.y)

	def getUpCell(self, cell):
		return self.getCell(cell.x, cell.y - 1)

	def getDownCell(self, cell):
		return self.getCell(cell.x, cell.y + 1)

	def setCellUpAsWall(self, cell):
		"""
		Update the map that put a wall above the given cell. 

		You may use this function by ``setCellUpWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		if cell != None:
			cell.setUpAsWall()
			cellUp = self.getUpCell(cell)
			if cellUp != None:
				cellUp.setDownAsWall()

	def setCellDownAsWall(self, cell):
		"""
		Update the map that put a wall below the given cell.

		You may use this function by ``setCellDownWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		if cell != None:
			cell.setDownAsWall()
			cellDown = self.getDownCell(cell)
			if cellDown != None:
				cellDown.setUpAsWall()

	def setCellLeftAsWall(self, cell):
		"""
		Update the map that put a wall on the left side of the given cell.

		You may use this function by ``setCellLeftWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		if cell != None:
			cell.setLeftAsWall()
			cellLeft = self.getLeftCell(cell)
			if cellLeft != None:
				cellLeft.setRightAsWall()

	def setCellRightAsWall(self, cell):
		"""
		Update the map that put a wall on the right side of the given cell.

		You may use this function by ``setCellRightWall(getCell(x, y))`` where *x* and *y* is the coordinates.
		"""
		if cell != None:
			cell.setRightAsWall()
			cellRight = self.getRightCell(cell)
			if cellRight != None:
				cellRight.setLeftAsWall()

	def readFromFile(self, mazeFile):
		"""
		Read and parse the maze file.

		The maze file example can be found `here <http://www.tcp4me.com/mmr/mazes/2018apec.maze>`_.
		The "|", "-" or "+" represents the vertical and horizontal walls.
		"""
		try:
			mazeFileReader = open(mazeFile, 'r')
			mazeLine = mazeFileReader.readlines()
			height = (int(len(mazeLine)/2))
			width = (int(len(mazeLine[0])/2-1))
			for i in range(height):
				for j in range(width):
					x = 2 * j + 1
					y = 2 * i + 1
					cell = self.getCell(j, i)
					cellLeftStr = mazeLine[y][x-1]
					cellUpStr = mazeLine[y-1][x]
					cellRightStr = mazeLine[y][x+1]
					cellDownStr = mazeLine[y+1][x]
					if cellLeftStr == '|':
						self.setCellLeftAsWall(cell)
					if cellUpStr == '-':
						self.setCellUpAsWall(cell)
					if cellRightStr == '|':
						self.setCellRightAsWall(cell)
					if cellDownStr == '-':
						self.setCellDownAsWall(cell)
			mazeFileReader.close()
		except:
			print('Open Maze File Error!')

