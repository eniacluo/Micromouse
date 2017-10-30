#!/usr/bin/env python3

#Author: Zhiwei Luo

from map import Map, MapDrawer
from tkinter import *

def TestMapAndCell():
	mapManager = Map(10, 10, 0, 0)

	cellTest = mapManager.getCell(0, 0)
	mapManager.setCellTopAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	mapManager.setCellDownAsWall(cellTest)

	print("00 " + cellTest.getWhichIsWall())

	cellTest = mapManager.getCell(1, 1)
	mapManager.setCellTopAsWall(cellTest)
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

def TestMapDrawer():
	mapManager = Map(10, 10, 40, 40)
	cellTest = mapManager.getCell(1, 1)
	mapManager.setCellTopAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellDownAsWall(cellTest)
	cellTest = mapManager.getCell(2, 1)
	mapManager.setCellTopAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	cellTest = mapManager.getCell(2, 2)
	mapManager.setCellDownAsWall(cellTest)
	mapManager.setCellLeftAsWall(cellTest)
	mapManager.setCellRightAsWall(cellTest)
	mapDrawer = MapDrawer(mapManager)
	mapDrawer.createWindow()
	mapDrawer.drawMap()
	mapDrawer.showWindow()

def TestMapReader():
	mapManager = Map(16, 16, 40, 40)
	mapManager.readFromFile('/home/zhiwei/Micromouse/mazes/95japx.txt')
	mapDrawer = MapDrawer(mapManager)
	mapDrawer.createWindow()
	mapDrawer.drawMap()
	mapDrawer.showWindow()

def TestUpdateMap():
	mapManager = Map(16, 16, 40, 40)
	mapManager.readFromFile('/home/zhiwei/Micromouse/mazes/2009japanb.txt')
	mapDrawer = MapDrawer(mapManager)
	mapDrawer.createWindow()
	mapDrawer.drawMap()
	mapDrawer.putRobotInCell(mapManager.getCell(0, 15), 'green')
	mapDrawer.putRobotInCell(mapManager.getCell(15, 0))
	mapDrawer.putRobotInCell(mapManager.getCell(0, 0), 'yellow')
	mapDrawer.putRobotInCell(mapManager.getCell(15, 15), 'blue')
	mapDrawer.showWindow()

#TestMapAndCell()
#TestMapDrawer()
#TestMapReader()
TestUpdateMap()
