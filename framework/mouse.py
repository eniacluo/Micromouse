#!/usr/bin/env python3

#Author: Zhiwei Luo

from controller import MotorController, SensorController

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
		return not self.mazeMap.getCellLeftWall(self.getCurrentCell())

	def canGoRight(self):
		return not self.mazeMap.getCellRightWall(self.getCurrentCell())

	def canGoUp(self):
		return not self.mazeMap.getCellUpWall(self.getCurrentCell())

	def canGoDown(self):
		return not self.mazeMap.getCellDownWall(self.getCurrentCell())

	def goLeft(self):
		self.commandTranslator.goLeft()
		self.x = self.x - 1
		self.direction = 'LEFT'

	def goRight(self):
		self.x = self.x + 1
		self.commandTranslator.goRight()
		self.direction = 'RIGHT'

	def goUp(self):
		self.y = self.y - 1
		self.commandTranslator.goUp()
		self.direction = 'UP'

	def goDown(self):
		self.y = self.y + 1
		self.commandTranslator.goDown()
		self.direction = 'DOWN'

	def senseWalls(self):
		cell = self.getCurrentCell()
		self.wallDetector.detectLeftWall(cell)
		self.wallDetector.detectRightWall(cell)
		self.wallDetector.detectUpWall(cell)
		self.wallDetector.detectDownWall(cell)

class TaskLoader:
    taskList = []

    def __init__(self):
        pass

    def addTask(self, task):
        self.taskList.append(task)

    def getTaskCount(self):
        return len(taskList)

    def start(self):
        for task in self.taskList:
            task.run()

class Task:
    strategy = None
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self):
        if self.strategy != None:
            while not self.strategy.checkFinished():
                self.strategy.go()

class CommandTranslator:
    motorController = None
    mouse = None

    def __init__(self, mouse, motorController=MotorController()):
        self.motorController = motorController
        self.mouse = mouse

    def goLeft(self):
        print('Go Left')
        if self.motorController != None:
            if not self.mouse.isTowardingLeft():
                if self.mouse.isTowardingUp():
                    self.motorController.turnLeft()
                if self.mouse.isTowardingRight():
                    self.motorController.turnAround()
                if self.mouse.isTowardingDown():
                    self.motorController.turnRight()
            self.motorController.goStraight()

    def goRight(self):
        print('Go Right')
        if self.motorController != None:
            if not self.mouse.isTowardingRight():
                if self.mouse.isTowardingUp():
                    self.motorController.turnRight()
                if self.mouse.isTowardingLeft():
                    self.motorController.turnAround()
                if self.mouse.isTowardingDown():
                    self.motorController.turnLeft()
            self.motorController.goStraight()

    def goUp(self):
        print('Go Up')
        if self.motorController != None:
            if not self.mouse.isTowardingUp():
                if self.mouse.isTowardingRight():
                    self.motorController.turnLeft()
                if self.mouse.isTowardingDown():
                    self.motorController.turnAround()
                if self.mouse.isTowardingLeft():
                    self.motorController.turnRight()
            self.motorController.goStraight()

    def goDown(self):
        print('Go Down')
        if self.motorController != None:
            if not self.mouse.isTowardingDown():
                if self.mouse.isTowardingLeft():
                    self.motorController.turnLeft()
                if self.mouse.isTowardingUp():
                    self.motorController.turnAround()
                if self.mouse.isTowardingRight():
                    self.motorController.turnRight()
            self.motorController.goStraight()

class WallDetector:
    sensorController = None
    mouse = None

    def __init__(self, mouse, sensorController=SensorController()):
        self.sensorController = sensorController
        self.mouse = mouse

    def detectLeftWall(self, cell):
        if self.sensorController != None:
            if self.mouse.isTowardingLeft():
                isLeftWall = self.sensorController.senseFront()
            elif self.mouse.isTowardingUp():
                isLeftWall = self.sensorController.senseLeft()
            elif self.mouse.isTowardingRight():
                isLeftWall = self.sensorController.senseBack()
            elif self.mouse.isTowardingDown():
                isLeftWall = self.sensorController.senseRight()

            if isLeftWall:
                self.mouse.mazeMap.setCellLeftAsWall(cell)

    def detectRightWall(self, cell):
        if self.sensorController != None:
            if self.mouse.isTowardingLeft():
                isRightWall = self.sensorController.senseBack()
            elif self.mouse.isTowardingUp():
                isRightWall = self.sensorController.senseRight()
            elif self.mouse.isTowardingRight():
                isRightWall = self.sensorController.senseFront()
            elif self.mouse.isTowardingDown():
                isRightWall = self.sensorController.senseLeft()
                
            if isRightWall:
                self.mouse.mazeMap.setCellRightAsWall(cell)

    def detectUpWall(self, cell):
        if self.sensorController != None:
            if self.mouse.isTowardingLeft():
                isUpWall = self.sensorController.senseRight()
            elif self.mouse.isTowardingUp():
                isUpWall = self.sensorController.senseFront()
            elif self.mouse.isTowardingRight():
                isUpWall = self.sensorController.senseLeft()
            elif self.mouse.isTowardingDown():
                isUpWall = self.sensorController.senseBack()
                
            if isUpWall:
                self.mouse.mazeMap.setCellUpAsWall(cell)

    def detectDownWall(self, cell):
        if self.sensorController != None:
            if self.mouse.isTowardingLeft():
                isDownWall = self.sensorController.senseLeft()
            elif self.mouse.isTowardingUp():
                isDownWall = self.sensorController.senseBack()
            elif self.mouse.isTowardingRight():
                isDownWall = self.sensorController.senseRight()
            elif self.mouse.isTowardingDown():
                isDownWall = self.sensorController.senseFront()
                
            if isDownWall:
                self.mouse.mazeMap.setCellDownAsWall(cell)
