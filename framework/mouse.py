#!/usr/bin/env python3

#Author: Zhiwei Luo

from task import TaskLoader, Task, CommandTranslator, WallDetector

class Micromouse:
	x = -1
	y = -1
	mazeMap = None
	taskLoader = None
	commandTranslator = None
	wallDetector = None
	direction = 'UP'
	isVisited = None

	def __init__(self, mazeMap):
		self.initMap(mazeMap)
		self.initTaskLoader()
		self.initCommandTranslator()
		self.initWallDetector()

	def setInitPoint(self, x, y):
		if self.x >= 0 and self.x < self.mazeMap.width:
			self.x = x
		else:
			self.x = 0

		if self.y >= 0 and self.y < self.mazeMap.height:
			self.y = y
		else:
			self.y = 0

	def initMap(self, mazeMap):
		self.mazeMap = mazeMap

	def initCommandTranslator(self):
		self.commandTranslator = CommandTranslator(self)

	def initWallDetector(self):
		self.wallDetector = WallDetector(self)

	def initTaskLoader(self):
		self.taskLoader = TaskLoader()

	def addTask(self, strategy):
		if self.taskLoader != None:
			self.taskLoader.addTask(Task(strategy))

	def run(self):
		if self.taskLoader != None:
			self.taskLoader.start()

	def isTowardingUp(self):
		return self.direction == 'UP'

	def isTowardingDown(self):
		return self.direction == 'DOWN'

	def isTowardingLeft(self):
		return self.direction == 'LEFT'

	def isTowardingRight(self):
		return self.direction == 'RIGHT'

	def getCurrentCell(self):
		return self.mazeMap.getCell(self.x, self.y)

	def goLeft(self):
		if not self.mazeMap.getCellLeftWall(self.getCurrentCell()):
			self.commandTranslator.goLeft()
			self.x = self.x - 1
			self.direction = 'LEFT'

	def goRight(self):
		if not self.mazeMap.getCellRightWall(self.getCurrentCell()):
			self.x = self.x + 1
			self.commandTranslator.goRight()
			self.direction = 'RIGHT'

	def goUp(self):
		if not self.mazeMap.getCellUpWall(self.getCurrentCell()):
			self.y = self.y - 1
			self.commandTranslator.goUp()
			self.direction = 'UP'

	def goDown(self):
		if not self.mazeMap.getCellDownWall(self.getCurrentCell()):
			self.y = self.y + 1
			self.commandTranslator.goDown()
			self.direction = 'DOWN'



