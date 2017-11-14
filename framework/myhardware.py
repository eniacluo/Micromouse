#!/usr/bin/env python3

#Author: Zhiwei Luo

import os
from hardware import MotorController

CORE_CELL_WIDTH = 72
CORE_CELL_HEIGHT = 48

class COREController(MotorController):
    
    direction = 'up'
    xpos = 42
    ypos = 25
    index = -1

    def __init__(self, index, initPoint):
        self.index = index
        self.xpos += initPoint[0] * CORE_CELL_WIDTH
        self.ypos += initPoint[1] * CORE_CELL_HEIGHT

    def turnLeft(self):
        print('Turn Left')
        if self.direction == 'up':
            self.direction = 'left'
        elif self.direction == 'left':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'right'
        else:
            self.direction = 'up'

    def turnRight(self):
        print('Turn Right')
        if self.direction == 'up':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'left'
        else:
            self.direction = 'up'

    def turnAround(self):
        print('Turn Around')
        if self.direction == 'up':
            self.direction = 'down'
        elif self.direction == 'right':
            self.direction = 'left'
        elif self.direction == 'down':
            self.direction = 'up'
        else:
            self.direction = 'right'

    def goStraight(self):
        print('direction: ' + self.direction)
        if self.direction == 'up':
            self.ypos -= CORE_CELL_HEIGHT
        elif self.direction == 'down':
            self.ypos += CORE_CELL_HEIGHT
        elif self.direction == 'left':
            self.xpos -= CORE_CELL_WIDTH
        else:
            self.xpos += CORE_CELL_WIDTH
        print("coresendmsg -a 10.0.0.254 node number=" + self.index + " xpos=" + str(self.xpos) + " ypos=" + str(self.ypos))
        os.system("coresendmsg -a 10.0.0.254 node number=" + self.index + " xpos=" + str(self.xpos) + " ypos=" + str(self.ypos))
