#!/usr/bin/env python3

#Author: Zhiwei Luo

from strategy import Strategy
from network import NetworkInterface
from time import sleep

class StrategyTestDFSDisplayEV3(Strategy):
	mouse = None
	isVisited = []
	path = []
	isBack = False

	def __init__(self, mouse):
		self.mouse = mouse
		self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
		self.isVisited[self.mouse.x][self.mouse.y] = 1
		self.network = NetworkInterface()
		self.network.initSocket()

	def checkFinished(self):
		return self.isBack

	def go(self):
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		sendData = {'x': self.mouse.x, 'y':self.mouse.y, 'up':self.mouse.canGoUp(), 'down':self.mouse.canGoDown(), 'left':self.mouse.canGoLeft(), 'right':self.mouse.canGoRight()}
		self.network.sendStringData(sendData)

		if self.mouse.canGoLeft() and not self.isVisited[self.mouse.x-1][self.mouse.y]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x-1][self.mouse.y] = 1
			self.mouse.goLeft()
		elif self.mouse.canGoUp() and not self.isVisited[self.mouse.x][self.mouse.y-1]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x][self.mouse.y-1] = 1
			self.mouse.goUp()
		elif self.mouse.canGoRight() and not self.isVisited[self.mouse.x+1][self.mouse.y]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x+1][self.mouse.y] = 1
			self.mouse.goRight()
		elif self.mouse.canGoDown() and not self.isVisited[self.mouse.x][self.mouse.y+1]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x][self.mouse.y+1] = 1
			self.mouse.goDown()
		else:
			if len(self.path) != 0:
				x, y = self.path.pop()
				if x < self.mouse.x:
					self.mouse.goLeft()
				elif x > self.mouse.x:
					self.mouse.goRight()
				elif y < self.mouse.y:
					self.mouse.goUp()
				elif y > self.mouse.y:
					self.mouse.goDown()
			else:
				self.isBack = True
