#!/usr/bin/env python3
from task import NetworkInterface
from map import Map
from map_painter import MapPainter

mazeMap = Map(16, 16)
mapPainter = MapPainter(mazeMap)
mapPainter.createWindow()
mapPainter.drawMap()
lastCell = mazeMap.getCell(0, 0)
mapPainter.putRobotInCell(lastCell, 'yellow')

network = NetworkInterface()
network.initSocket()
network.startReceiveThread()

while True:
	recvData = network.retrieveData()
	if recvData:
		otherMap = recvData
		cell = mazeMap.getCell(otherMap['x'], otherMap['y'])
		if otherMap['up']: mazeMap.setCellUpAsWall(cell)
		if otherMap['down']: mazeMap.setCellDownAsWall(cell)
		if otherMap['left']: mazeMap.setCellLeftAsWall(cell)
		if otherMap['right']: mazeMap.setCellRightAsWall(cell)
		mapPainter.drawCell(cell, 'grey')
		mapPainter.putRobotInCell(lastCell)
		mapPainter.putRobotInCell(cell, 'yellow')
		lastCell = cell
		print('('+str(otherMap['x'])+', '+str(otherMap['y'])+')  up:'+str(otherMap['up'])+',down:'+str(otherMap['down'])+',left:'+str(otherMap['left'])+'right:'+str(otherMap['right']))
