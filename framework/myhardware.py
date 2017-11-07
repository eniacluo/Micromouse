#!/usr/bin/env python3

#Author: Zhiwei Luo

import os

class COREController(MotorController):
    direction = 'up'
    xpos = 42
    ypos = 25

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
            self.ypos -= 48
        elif self.direction == 'down':
            self.ypos += 48
        elif self.direction == 'left':
            self.xpos -= 72
        else:
            self.xpos += 72
        print("coresendmsg -a 10.0.0.254 node number=1 xpos="+str(self.xpos)+" ypos="+str(self.ypos))
        os.system("coresendmsg -a 10.0.0.254 node number=1 xpos="+str(self.xpos)+" ypos="+str(self.ypos))
