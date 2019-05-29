#!/usr/bin/env python3
from network import NetworkInterface
from map import Map, Cell
from tkinter import Tk, Canvas

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
		self.height = 40
		self.width = 40
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

if __name__ == '__main__':
	mazeMap = Map(16, 16)
	mapPainter = MapPainter(mazeMap)
	mapPainter.createWindow()
	mapPainter.drawMap()
	lastCell = mazeMap.getCell(0, 0)
	mapPainter.putRobotInCell(lastCell, 'yellow')

	network = NetworkInterface()
	network.initSocket()
	network.startReceiveThread()

	while True:
		recvData = network.retrieveData()
		if recvData:
			otherMap = recvData
			cell = mazeMap.getCell(otherMap['x'], otherMap['y'])
			if otherMap['up']: mazeMap.setCellUpAsWall(cell)
			if otherMap['down']: mazeMap.setCellDownAsWall(cell)
			if otherMap['left']: mazeMap.setCellLeftAsWall(cell)
			if otherMap['right']: mazeMap.setCellRightAsWall(cell)
			mapPainter.drawCell(cell, 'grey')
			mapPainter.putRobotInCell(lastCell)
			mapPainter.putRobotInCell(cell, 'yellow')
			lastCell = cell
			print('('+str(otherMap['x'])+', '+str(otherMap['y'])+')  up:'+str(otherMap['up'])+',down:'+str(otherMap['down'])+',left:'+str(otherMap['left'])+'right:'+str(otherMap['right']))
