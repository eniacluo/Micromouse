#!/usr/bin/env python3

#Author: Zhiwei Luo

from map import Map
from mouse import Micromouse
from strategy import StrategyTestMultiDFS
from controller import COREController
from socket import *

mazeMap = Map(16, 16, 40, 40)
mazeMap.readFromFile('/home/zhiwei/Micromouse/mazes/2012japan-ef.txt')
micromouse = Micromouse(mazeMap)
myIPAddr = gethostbyname(gethostname())
index = myIPAddr.split('.')[3]
initPoint = {'1':(0,0), '2':(15,0), '3':(0,15), '4':(15,15)}
micromouse.setMotorController(COREController(index, initPoint[index]))
micromouse.setInitPoint(initPoint[index][0], initPoint[index][1])
micromouse.addTask(StrategyTestMultiDFS(micromouse))
micromouse.run()