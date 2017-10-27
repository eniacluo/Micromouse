#!/usr/bin/env python3

#Author: Zhiwei Luo

from cell import Cell

class Map:
	height = 0
	width = 0
	cellHeight = 0
	cellWidth = 0
	cells = None

	def __init__(self, height, width, cellHeight, cellWidth):
		self.height = height
		self.width = width
		self.cellHeight = cellHeight
		self.cellWidth = cellWidth
		self.cells = [[Cell(j, i) for i in range(width)] for j in range(height)]

	def getCell(self, x, y):
		if x >= 0 and y >= 0 and x < self.width and y < self.height:
			return self.cells[x][y]
		else:
			return None

	def setCellTopAsWall(self, cell):
		if cell != None:
			cell.setTopAsWall()
			self.getTopCell(cell).setDownAsWall()

	def setCellDownAsWall(self, cell):
		if cell != None:
			cell.setDownAsWall()
			self.getDownCell(cell).setTopAsWall()

	def setCellLeftAsWall(self, cell):
		if cell != None:
			cell.setLeftAsWall()
			self.getLeftCell(cell).setCellRightAsWall()

	def setCellRightAsWall(self, cell):
		if cell != None:
			cell.setRightAsWall()
			self.getRightCell(cell).setLeftAsWall()

	def getCellTopWall(self, cell):
		return cell.hasTopWall

	def getCellDownWall(self, cell):
		return cell.hasDownWall

	def getCellLeftWall(self, cell):
		return cell.hasLeftWall

	def getCellRightWall(self, cell):
		return cell.hasRightWall

	def getRightCell(self, cell):
		return self.getCell(cell.x + 1, cell.y)

	def getLeftCell(self, cell):
		return self.getCell(cell.x - 1, cell.y)

	def getTopCell(self, cell):
		return self.getCell(cell.x, cell.y - 1)

	def getDownCell(self, cell):
		return self.getCell(cell.x, cell.y + 1)

	def clearAllCells():
		for i in range(height):
			for j in range(width):
				self.getCell(i, j).setAllAsNoWall()


