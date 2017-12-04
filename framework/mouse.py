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

	def __init__(self, mazeMap):
		self.initMap(mazeMap)
		self.initTaskLoader()
		self.initCommandTranslator()
		self.initWallDetector()

	def setInitPoint(self, x, y):
		if x >= 0 and x < self.mazeMap.width:
			self.x = x
		else:
			self.x = 0

		if y >= 0 and y < self.mazeMap.height:
			self.y = y
		else:
			self.y = 0
	def setInitDirection(self, direction):
		if direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
			self.direction = direction

	def initMap(self, mazeMap):
		self.mazeMap = mazeMap

	def initCommandTranslator(self):
		self.commandTranslator = CommandTranslator(self)

	def initWallDetector(self):
		self.wallDetector = WallDetector(self)

	def setMotorController(self, motorController):
		self.commandTranslator = CommandTranslator(self, motorController)

	def setSensorController(self, sensorController):
		self.wallDetector = WallDetector(self, sensorController)

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

	def canGoLeft(self):
		return self.mazeMap.getCellLeftWall(self.getCurrentCell())

	def canGoRight(self):
		return self.mazeMap.getCellRightWall(self.getCurrentCell())

	def canGoUp(self):
		return self.mazeMap.getCellUpWall(self.getCurrentCell())

	def canGoDown(self):
		return self.mazeMap.getCellDownWall(self.getCurrentCell())

	def goLeft(self):
		if not self.canGoLeft():
			self.commandTranslator.goLeft()
			self.x = self.x - 1
			self.direction = 'LEFT'

	def goRight(self):
		if not self.canGoRight():
			self.x = self.x + 1
			self.commandTranslator.goRight()
			self.direction = 'RIGHT'

	def goUp(self):
		if not self.canGoUp():
			self.y = self.y - 1
			self.commandTranslator.goUp()
			self.direction = 'UP'

	def goDown(self):
		if not self.canGoDown():
			self.y = self.y + 1
			self.commandTranslator.goDown()
			self.direction = 'DOWN'

	def senseWalls(self):
		cell = self.getCurrentCell()
		self.wallDetector.detectLeftWall(cell)
		self.wallDetector.detectRightWall(cell)
		self.wallDetector.detectUpWall(cell)
		self.wallDetector.detectDownWall(cell)


