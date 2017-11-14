#!/usr/bin/env python3

#Author: Zhiwei Luo

from map import Map, MapPainter
from tkinter import *
from mystrategy import StrategyTestProgress, StrategyTestCount, StrategyTestGoDown, StrategyTestDFS, StrategyTestMultiDFS
from mouse import Micromouse
import threading
from task import CommandTranslator, NetworkInterface
from myhardware import COREController
from socket import *

def TestMapAndCell():
	mapManager = Map(10, 10, 0, 0)

	cellTest = mapManager.getCell(0, 0)
	mapManager.setCellUpAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	mapManager.setCellDownAsWall(cellTest)

	print("00 " + cellTest.getWhichIsWall())

	cellTest = mapManager.getCell(1, 1)
	mapManager.setCellUpAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	mapManager.setCellDownAsWall(cellTest)

	print("11 " + cellTest.getWhichIsWall())

	cellTest01 = mapManager.getCell(0, 1)
	cellTest10 = mapManager.getCell(1, 0)

	print("01 " + cellTest01.getWhichIsWall())
	print("10 " + cellTest10.getWhichIsWall())

	mapManager.clearAllCells()
	print("00 " + cellTest.getWhichIsWall())

def TestMapPainter():
	mapManager = Map(10, 10, 40, 40)
	cellTest = mapManager.getCell(1, 1)
	mapManager.setCellUpAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellDownAsWall(cellTest)
	cellTest = mapManager.getCell(2, 1)
	mapManager.setCellUpAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	cellTest = mapManager.getCell(2, 2)
	mapManager.setCellDownAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	mapPainter = MapPainter(mapManager)
	mapPainter.createWindow()
	mapPainter.drawMap()
	mapPainter.showWindow()

def TestMapReader():
	mapManager = Map(16, 16, 40, 40)
	mapManager.readFromFile('/home/zhiwei/Micromouse/mazes/95japx.txt')
	mapPainter = MapPainter(mapManager)
	mapPainter.createWindow()
	mapPainter.drawMap()
	mapPainter.showWindow()

def TestUpdateMap():
	mapManager = Map(16, 16, 40, 40)
	mapManager.readFromFile('/home/zhiwei/Micromouse/mazes/2009japanb.txt')
	mapPainter = MapPainter(mapManager)
	mapPainter.createWindow()
	mapPainter.drawMap()
	mapPainter.putRobotInCell(mapManager.getCell(0, 15), 'green')
	mapPainter.putRobotInCell(mapManager.getCell(15, 0))
	mapPainter.putRobotInCell(mapManager.getCell(0, 0), 'yellow')
	mapPainter.putRobotInCell(mapManager.getCell(15, 15), 'blue')
	mapPainter.showWindow()

def TestStrategyGo():
	mazeMap = Map(16, 16, 40, 40)
	mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/95japx.txt')
	micromouse = Micromouse(mazeMap)
	micromouse.setInitPoint(0, 0)
	micromouse.addTask(StrategyTestProgress())
	micromouse.addTask(StrategyTestCount())
	micromouse.run()

def TestStrategyGoDownThread():
	threading.Thread(target=TestStrategyGoDown).start()
	mapPainter.showWindow()

def TestStrategyGoDown():
	mazeMap = Map(16, 16, 40, 40)
	mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/2009japanb.txt')
	mapPainter = MapPainter(mazeMap)
	mapPainter.createWindow()
	mapPainter.drawMap()
	mapPainter.putRobotInCell(mazeMap.getCell(0, 0), 'yellow')
	micromouse = Micromouse(mazeMap)
	micromouse.setInitPoint(0, 0)
	micromouse.addTask(StrategyTestGoDown(micromouse, mapPainter))
	micromouse.run()

def TestStrategyDFS():
	mazeMap = Map(16, 16, 40, 40)
	mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/2009japanb.txt')
	mapPainter = MapPainter(mazeMap)
	mapPainter.createWindow()
	mapPainter.drawMap()
	mapPainter.putRobotInCell(mazeMap.getCell(0, 0), 'yellow')
	micromouse = Micromouse(mazeMap)
	micromouse.setInitPoint(0, 0)
	micromouse.addTask(StrategyTestDFS(micromouse, mapPainter))
	micromouse.run()

def TestInterface():
	networkInterface = NetworkInterface()
	networkInterface.initSocket()
	import sys
	import _pickle as pickle
	import time
	if sys.argv[1] == 'r':
		networkInterface.startReceiveThread()
		c = 0
		while c < 10:
			recv = networkInterface.retrieveData()
			if recv:
				print(type(pickle.loads(recv)), pickle.loads(recv))
			time.sleep(1)
			c += 1

	if sys.argv[1] == 's':
		networkInterface.sendStringData()

def TestStrategyMultiDFS():
	mazeMap = Map(16, 16, 40, 40)
	mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/2009japanb.txt')
	mapPainter = MapPainter(mazeMap)
	#mapPainter.createWindow()
	#mapPainter.drawMap()
	#mapPainter.putRobotInCell(mazeMap.getCell(0, 0), 'yellow')
	micromouse = Micromouse(mazeMap)
	import sys
	if sys.argv[1] == '0':
		micromouse.setInitPoint(0, 0)
	if sys.argv[1] == '1':
		micromouse.setInitPoint(15, 0)
	micromouse.addTask(StrategyTestMultiDFS(micromouse, mapPainter))
	micromouse.run()

def TestStrategyInCORE():
	mazeMap = Map(16, 16, 40, 40)
	mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/2012japan-ef.txt')
	mapPainter = MapPainter(mazeMap)
	#mapPainter.createWindow()
	#mapPainter.drawMap()
	#mapPainter.putRobotInCell(mazeMap.getCell(0, 0), 'yellow')
	micromouse = Micromouse(mazeMap)
	myIPAddr = gethostbyname(gethostname())
	index = myIPAddr.split('.')[3]
	initPoint = {'1':(0,0), '2':(15,0), '3':(0,15), '4':(15,15)}
	micromouse.commandTranslator = CommandTranslator(micromouse, COREController(index, initPoint[index]))
	micromouse.setInitPoint(initPoint[index][0], initPoint[index][1])
	micromouse.addTask(StrategyTestMultiDFS(micromouse, mapPainter))
	micromouse.run()

#TestMapAndCell()
#TestMapPainter()
#TestMapReader()
#TestUpdateMap()
#TestStrategyGo()
#TestStrategyGoDown()
#TestStrategyDFS()
#TestInterface()
#TestStrategyMultiDFS()
TestStrategyInCORE()