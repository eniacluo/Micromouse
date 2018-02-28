#!/usr/bin/env python3

#Author: Zhiwei Luo

import os
#from ev3dev.ev3 import *

CORE_CELL_WIDTH = 72
CORE_CELL_HEIGHT = 48

class MotorController:
    def turnLeft(self):
        pass

    def turnRight(self):
        pass

    def turnAround(self):
        pass

    def goStraight(self):
        pass

class SensorController:
    def senseLeft(self):
        return False

    def senseRight(self):
        return False

    def senseFront(self):
        return False

    def senseBack(self):
        return False

class COREController(MotorController):
    
    direction = 'up'
    xpos = 42
    ypos = 25
    index = -1

    def __init__(self, index, initPoint, controlNet):
        self.index = index
        self.xpos += initPoint[0] * CORE_CELL_WIDTH
        self.ypos += initPoint[1] * CORE_CELL_HEIGHT
        self.controlNet = controlNet

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
        print("coresendmsg -a " + controlNet + " node number=" + self.index + " xpos=" + str(self.xpos) + " ypos=" + str(self.ypos))
        os.system("coresendmsg -a " + controlNet + " node number=" + self.index + " xpos=" + str(self.xpos) + " ypos=" + str(self.ypos))

class EV3MotorController(MotorController):
    direction = 'up'    
    direc = 0           # angle used for gyro, direction adjustment
    backturnp = 0       # used as flag to 0-left or 1-right to turn around

    def __init__(self):
        self.ir = UltrasonicSensor('in4')
        self.left = UltrasonicSensor('in2')
        self.right = UltrasonicSensor('in3')
        self.motorR = Motor('outC')
        self.motorL = Motor('outB')
        self.gy = GyroSensor('in1')

    def turnLeft(self):
        print('Turn Left')
        self.direc += 90
        self.motorL.run_direct(duty_cycle_sp=-30)
        self.motorR.run_direct(duty_cycle_sp=30)
        while(True):
            ang,rt = self.gy.rate_and_angle
            if self.gy.value() >= self.direc - 15 and self.gy.value() < self.direc:
                self.motorL.run_direct(duty_cycle_sp=-20)
                self.motorR.run_direct(duty_cycle_sp=20)
            elif self.gy.value() < self.direc and rt == 0:
                self.motorL.run_direct(duty_cycle_sp=-25)
                self.motorR.run_direct(duty_cycle_sp=25)
            elif self.gy.value() >= self.direc:
                self.motorR.stop(stop_action='hold')
                self.motorL.stop(stop_action='hold')
                break
        self.adjust_stable()

    def turnRight(self):
        print('Turn Right')
        self.direc -= 90
        self.motorL.run_direct(duty_cycle_sp=30)
        self.motorR.run_direct(duty_cycle_sp=-30)
        while(True):
            ang,rt = self.gy.rate_and_angle
            if self.gy.value() <= self.direc + 15 and self.gy.value() > self.direc:
                self.motorL.run_direct(duty_cycle_sp=20)
                self.motorR.run_direct(duty_cycle_sp=-20)
            elif self.gy.value() > self.direc and rt == 0:
                self.motorL.run_direct(duty_cycle_sp=25)
                self.motorR.run_direct(duty_cycle_sp=-25)
            elif self.gy.value() <= self.direc:
                self.motorR.stop(stop_action='hold')
                self.motorL.stop(stop_action='hold')
                break
        self.adjust_stable()

    def turnAround(self):
        print('Turn Around')
        # Going left and going right by turn because of the feature of gyro
        if self.backturnp % 2:
            self.direc += 180
            self.motorL.run_direct(duty_cycle_sp=-30)
            self.motorR.run_direct(duty_cycle_sp=30)
            while(True):
                ang,rt = self.gy.rate_and_angle
                if self.gy.value() >= self.direc - 15 and self.gy.value() < self.direc:
                    self.motorL.run_direct(duty_cycle_sp=-20)
                    self.motorR.run_direct(duty_cycle_sp=20)
                elif ang < self.direc and rt == 0:
                    #rt=0 means velocity=0 && < : not there
                    self.motorL.run_direct(duty_cycle_sp=-25)
                    self.motorR.run_direct(duty_cycle_sp=25)
                elif self.gy.value() >= self.direc:
                    self.motorR.stop(stop_action='hold')
                    self.motorL.stop(stop_action='hold')
                    break
            self.adjust_stable()
        else:
            self.direc -= 180
            self.motorL.run_direct(duty_cycle_sp=30)
            self.motorR.run_direct(duty_cycle_sp=-30)
            while(True):
                ang,rt = self.gy.rate_and_angle
                if self.gy.value() <= self.direc + 15 and self.gy.value() > self.direc:
                    self.motorL.run_direct(duty_cycle_sp=20)
                    self.motorR.run_direct(duty_cycle_sp=-20)
                elif ang > self.direc and rt == 0:
                    self.motorL.run_direct(duty_cycle_sp=25)
                    self.motorR.run_direct(duty_cycle_sp=-25)
                elif self.gy.value() <= self.direc:
                    self.motorR.stop(stop_action='hold')
                    self.motorL.stop(stop_action='hold')
                    break
            self.adjust_stable()
        self.backturnp += 1
        if self.backturnp % 2 == 0:
            time.sleep(2.8)
            self.gyreset()

    def goStraight(self):
        print("Go Straight")
        startT = time.time()
        lold = self.left.value()
        rold = self.right.value()
        while(True):
            if self.gy.value() > self.direc:
                self.motorR.run_direct(duty_cycle_sp=66)
                self.motorL.run_direct(duty_cycle_sp=74)
            if self.gy.value() < self.direc:
                self.motorR.run_direct(duty_cycle_sp=74)
                self.motorL.run_direct(duty_cycle_sp=66)
            if self.gy.value() == self.direc:
                self.motorR.run_direct(duty_cycle_sp=70)
                self.motorL.run_direct(duty_cycle_sp=70)
            if time.time() - startT > 1.35:
                if self.gy.value() > self.direc:
                    self.motorR.run_direct(duty_cycle_sp=38)
                    self.motorL.run_direct(duty_cycle_sp=42)
                if self.gy.value() < self.direc:
                    self.motorR.run_direct(duty_cycle_sp=42)
                    self.motorL.run_direct(duty_cycle_sp=38)
                if self.gy.value() == self.direc:
                    self.motorR.run_direct(duty_cycle_sp=40)
                    self.motorL.run_direct(duty_cycle_sp=40)
            if time.time() - startT > 1.55:
                self.motorR.run_direct(duty_cycle_sp=15)
                self.motorL.run_direct(duty_cycle_sp=15)
            lold, rold = self.direchange(lold, rold)
            if time.time() - startT > 1.7:
                self.motorR.stop(stop_action='hold')
                self.motorL.stop(stop_action='hold')
                self.adjust_stable()
                break;

    #When finishing a movement, adjust the direction to the navigation direction
    def adjust_stable(self):
        while(True):
            ang,rt = self.gy.rate_and_angle
            #print(str(r) + ' ' + str(a) + ' ' + str(direc))
            if self.gy.value() > self.direc + 1.2:
                if rt == 0:
                    self.motorR.run_direct(duty_cycle_sp=-25)
                    self.motorL.run_direct(duty_cycle_sp=25)
                else:
                    self.motorR.run_direct(duty_cycle_sp=-15)
                    self.motorL.run_direct(duty_cycle_sp=15)
            elif self.gy.value() < self.direc - 1.2:
                if rt == 0:
                    self.motorR.run_direct(duty_cycle_sp=25)
                    self.motorL.run_direct(duty_cycle_sp=-25)
                else:
                    self.motorR.run_direct(duty_cycle_sp=15)
                    self.motorL.run_direct(duty_cycle_sp=-15)
            elif self.gy.value() >= self.direc - 2 and self.gy.value() <= self.direc + 2:
                time.sleep(0.1)
                if rt <= 15 and rt >= -15:
                    self.motorR.stop(stop_action='hold')
                    self.motorL.stop(stop_action='hold')
                    break
                continue

    #Change the navigating direction as it goes to avoid drift as much as possible
    def direchange(self, lold, rold):
        l = self.left.value()
        r = self.right.value()
        if (l < 75 and l + r > 130 and l <= lold + 1) or (l > 2400):
            self.direc -= 0.2
            lold = l
            rold = r
        if (r < 75 and l + r > 130 and r <= rold + 1) or (r > 2400):
            self.direc += 0.2
            lold = l
            rold = r
        return lold, rold

    #Re-caliberate gyro sensor
    def gyreset(self):
        self.gy.mode = 'GYRO-RATE'
        self.gy.mode = 'GYRO-G&A'
        while(True):
            ang,rt = self.gy.rate_and_angle
            if(ang == 0 and rt == 0):
                break
        self.direc = self.gy.value()

class EV3SensorController(SensorController):

    def __init__(self):
        self.front = UltrasonicSensor('in4')
        self.left = UltrasonicSensor('in2')
        self.right = UltrasonicSensor('in3')

    def senseLeft(self):
        l = self.left.value()
        if l < 180 and l > 10:
            return True
        else:
            return False

    def senseRight(self):
        r = self.right.value()
        if r < 180 and r > 10:
            return True
        else:
            return False

    def senseFront(self):
        f = self.front.value()
        if f < 180 and f > 10:
            return True
        else:
            return False

    def senseBack(self):
        return False