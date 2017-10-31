#!/usr/bin/env python3

#Author: Zhiwei Luo

from hardware import MotorController, SensorController

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

class Strategy:
	def checkFinished(self):
		return True

	def go(self):
		pass

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
				self.motorController.turnAround()
			elif self.mouse.isTowardingUp():
				self.motorController.turnRight()
			elif self.mouse.isTowardingRight():
				pass
			elif self.mouse.isTowardingDown():
				self.motorController.turnLeft()
			self.motorController.goStraight()

	def goUp(self):
		print('Go Up')
		if self.motorController != None:
			if not self.mouse.isTowardingUp():
				self.motorController.turnRight()
			elif self.mouse.isTowardingUp():
				pass
			elif self.mouse.isTowardingRight():
				self.motorController.turnleft()
			elif self.mouse.isTowardingDown():
				self.motorController.turnAround()
			self.motorController.goStraight()

	def goDown(self):
		print('Go Down')
		if self.motorController != None:
			if not self.mouse.isTowardingDown():
				self.motorController.turnLeft()
			elif self.mouse.isTowardingUp():
				self.motorController.turnAround()
			elif self.mouse.isTowardingRight():
				self.motorController.turnRight()
			elif self.mouse.isTowardingDown():
				pass
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

class NetworkInterface:
	def Establish():
		pass
