#!/usr/bin/env python3
"""
	*mouse* module contains *class* **Micromouse**.
"""

#Author: Zhiwei Luo

from controller import MotorController, SensorController

class Micromouse:
	"""
	The Micromouse represents an agent to perfrom tasks. It maintains:
		* the location in a maze: *x*, *y*
		* a local *map*
		* a *task loader*
		* the *direction* it faces: "UP", "DOWN", "LEFT", or "RIGHT"

	Before creating a new **Micromouse**, you may need to create an empty maze map and put this map to create the Micromouse.
	"""
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

	def setInitPoint(self, x=-1, y=-1):
		"""
			The initial location (x, y) you put micromouse in the map of a maze.

			The coordinate system set the left-top corner as (0, 0):

				+-----+-----+-----+
				|(0,0)|(1,0)|(2,0)|
				+-----+-----+-----+
				|(0,1)|(1,1)| ... |
				+-----+-----+-----+
				|(0,2)| ... | ... |
				+-----+-----+-----+

			The x, y will be set failed if it is out of the boundary of maze map.
			The **default** location is (-1, -1).
		"""
		if x >= 0 and x < self.mazeMap.width:
			self.x = x
		else:
			self.x = 0

		if y >= 0 and y < self.mazeMap.height:
			self.y = y
		else:
			self.y = 0
	def setInitDirection(self, direction="UP"):
		"""
			The initial direction you put micromouse in the maze. 

			The direction should be "UP", "DOWN", "LEFT", or "RIGHT".
			The **default** direction is *"UP"*.
		"""
		if direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
			self.direction = direction

	def initMap(self, mazeMap):
		self.mazeMap = mazeMap

	def initCommandTranslator(self):
		self.commandTranslator = CommandTranslator(self)

	def initWallDetector(self):
		self.wallDetector = WallDetector(self)

	def setMotorController(self, motorController):
		"""
			Specify the MotorController for this micromouse.

			Your MotorController should inherit the *class* **MotorController** and overrides the function *turnLeft()*, *turnRight()*, *turnAround()*, *goStraight()*.
		"""
		self.commandTranslator = CommandTranslator(self, motorController)

	def setSensorController(self, sensorController):
		"""
			Specify the SensorController for this micromouse.

			Your SensorController should inherit the *class* **SensorController** and overrides the function *senseLeft()*, *senseRight()*, *senseUp()*, *senseDown()*.
		"""
		self.wallDetector = WallDetector(self, sensorController)

	def initTaskLoader(self):
		self.taskLoader = TaskLoader()

	def addTask(self, strategy):
		"""
			Add one task to the task list such that task loader will execute the tasks in sequence.

			The task is the wrapper of a strategy. You need to put your Strategy as argument.
		"""
		if self.taskLoader != None:
			self.taskLoader.addTask(Task(strategy))

	def run(self):
		"""
			Start to run your tasks by your strategies in the maze.
		"""
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
		"""
			Return True if there is no wall on the left of your micromouse, and False vice versa.
		"""
		return not self.mazeMap.getCellLeftWall(self.getCurrentCell())

	def canGoRight(self):
		"""
			Return True if there is no wall on the right of your micromouse, and False vice versa.
		"""
		return not self.mazeMap.getCellRightWall(self.getCurrentCell())

	def canGoUp(self):
		"""
			Return True if there is no wall above your micromouse, and False vice versa.
		"""
		return not self.mazeMap.getCellUpWall(self.getCurrentCell())

	def canGoDown(self):
		"""
			Return True if there is no wall below your micromouse, and False vice versa.
		"""
		return not self.mazeMap.getCellDownWall(self.getCurrentCell())

	def goLeft(self):
		"""
			Go to the Left immediate cell of your current location.

			As a result, x := x - 1 and direction will be "LEFT".
		"""
		self.commandTranslator.goLeft()
		self.x = self.x - 1
		self.direction = 'LEFT'

	def goRight(self):
		"""
			Go to the Right immediate cell of your current location.

			As a result, x := x + 1 and direction will be "RIGHT".
		"""
		self.x = self.x + 1
		self.commandTranslator.goRight()
		self.direction = 'RIGHT'

	def goUp(self):
		"""
			Go up to the immediate cell of your current location.

			As a result, y := y - 1 and direction will be "UP".
		"""
		self.y = self.y - 1
		self.commandTranslator.goUp()
		self.direction = 'UP'

	def goDown(self):
		"""
			Go Down to the immediate cell of your current location.

			As a result, y := y + 1 and direction will be "DOWN".
		"""
		self.y = self.y + 1
		self.commandTranslator.goDown()
		self.direction = 'DOWN'

	def senseWalls(self):
		"""
			Use Wall Detector to detector the surrounding walls. If sensors find the walls, the micromouse will update the local map.

			You may need to call this function when your micromouse arrives at a cell that has never been visited.
		"""
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
