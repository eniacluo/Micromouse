#!/usr/bin/env python3

#Author: Zhiwei Luo

from cell import Cell
from tkinter import Tk, Canvas

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

	def getCellUpWall(self, cell):
		return cell.hasUpWall

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

	def getUpCell(self, cell):
		return self.getCell(cell.x, cell.y - 1)

	def getDownCell(self, cell):
		return self.getCell(cell.x, cell.y + 1)

	def setCellUpAsWall(self, cell):
		if cell != None:
			cell.setUpAsWall()
			cellUp = self.getUpCell(cell)
			if cellUp != None:
				cellUp.setDownAsWall()

	def setCellDownAsWall(self, cell):
		if cell != None:
			cell.setDownAsWall()
			cellDown = self.getDownCell(cell)
			if cellDown != None:
				cellDown.setUpAsWall()

	def setCellLeftAsWall(self, cell):
		if cell != None:
			cell.setLeftAsWall()
			cellLeft = self.getLeftCell(cell)
			if cellLeft != None:
				cellLeft.setRightAsWall()

	def setCellRightAsWall(self, cell):
		if cell != None:
			cell.setRightAsWall()
			cellRight = self.getRightCell(cell)
			if cellRight != None:
				cellRight.setLeftAsWall()

	def readFromFile(self, mazeFile):
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

	def clearAllCells(self):
		for i in range(self.height):
			for j in range(self.width):
				self.getCell(i, j).setAllAsNoWall()


class MapPainter:
	height = 0
	width = 0
	mapDraw = None
	window = None
	canvas = None

	def __init__(self):
		self.height = 40
		self.width = 40

	def __init__(self, mapDraw):
		self.height = mapDraw.cellHeight
		self.width = mapDraw.cellWidth
		self.mapDraw = mapDraw

	def setCellHeight(self, height):
		self.height = height

	def setCellWidth(self, height):
		self.width = width

	def createWindow(self):
		if self.mapDraw != None:
			self.window = Tk()
			self.canvas = Canvas(self.window, width=self.mapDraw.width*40, height=self.mapDraw.height*40)
			self.canvas.pack()
		else:
			print('No Map is available to paint!')

	def showWindow(self):
		self.window.mainloop()

	def drawMap(self):
		for i in range(self.mapDraw.height):
			for j in range(self.mapDraw.width):
				self.drawCell(self.mapDraw.getCell(j, i))

	def drawCell(self, cell, color='white'):
		if cell != None:
			leftUpX = cell.x * self.width
			leftUpY = cell.y * self.height
			leftDownX = cell.x * self.width
			leftDownY = (cell.y + 1) * self.height
			rightUpX = (cell.x + 1) * self.width
			rightUpY = cell.y * self.height
			rightDownX = (cell.x + 1) * self.width
			rightDownY = (cell.y + 1) * self.height
			self.canvas.create_rectangle(leftUpX, leftUpY, rightDownX, rightDownY, fill=color, outline='white')
			if cell.hasLeftWall:
				self.canvas.create_line(leftUpX, leftUpY, leftDownX, leftDownY, fill='black',width=3)
			if cell.hasRightWall:
				self.canvas.create_line(rightUpX, rightUpY, rightDownX, rightDownY, fill='black',width=3)
			if cell.hasUpWall:
				self.canvas.create_line(leftUpX, leftUpY, rightUpX, rightUpY, fill='black',width=3)
			if cell.hasDownWall:
				self.canvas.create_line(leftDownX, leftDownY, rightDownX, rightDownY, fill='black',width=3)
			self.canvas.update()

	def clearCellWithMap(self, cell):
		if cell != None:
			drawCell(cell)

	def putRobotInCell(self, cell, color='red', border=10):
		if cell != None:
			self.drawCell(cell)
			leftUpX = cell.x * self.width + border
			leftUpY = cell.y * self.height + border
			rightDownX = (cell.x + 1) * self.width - border
			rightDownY = (cell.y + 1) * self.height - border
			self.canvas.create_rectangle(leftUpX, leftUpY, rightDownX, rightDownY, fill=color, outline='white')
			self.canvas.update()
