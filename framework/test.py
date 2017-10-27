#!/usr/bin/env python3

#Author: Zhiwei Luo

from map import Map

mapManager = Map(10, 10, 0, 0)

cellTest = mapManager.getCell(1, 1)

print(cellTest.getWhichIsWall())

print(cellTest.x)
print(cellTest.y)

mapManager.setCellTopAsWall(cellTest)
	
