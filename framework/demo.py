#!/usr/bin/env python3

#Author: Zhiwei Luo

from map import Map
from mouse import Micromouse
from strategy import StrategyTestInitEV3, StrategyTestMultiDFS
from controller import EV3MotorController, EV3SensorController

mazeMap = Map(8, 8, 40, 40)
micromouse = Micromouse(mazeMap)
micromouse.setMotorController(EV3MotorController())
micromouse.setSensorController(EV3SensorController())
micromouse.setInitDirection("UP")
micromouse.setInitPoint(2, 7)
micromouse.addTask(StrategyTestInitEV3(micromouse))
micromouse.addTask(StrategyTestMultiDFS(micromouse))
micromouse.run()