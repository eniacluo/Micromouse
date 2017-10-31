#!/usr/bin/env python3

#Author: Zhiwei Luo

from map import Map, MapPainter
from tkinter import *
from mystrategy import StrategyTestProgress, StrategyTestCount, StrategyTestGoDown, StrategyTestDFS
from mouse import Micromouse
import threading

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

#TestMapAndCell()
#TestMapPainter()
#TestMapReader()
#TestUpdateMap()
#TestStrategyGo()
#TestStrategyGoDown()
TestStrategyDFS()