#!/usr/bin/env python3

#Author: Yang Shi

#Please see the coding of walls in ./RepresentationofWalls.ods .
leftlist = [0,1,2,4,5,8,10,14]
rightlist = [0,1,2,3,5,7,9,13]
uplist = [0,2,3,4,6,9,10,11]
downlist = [0,1,3,4,6,7,8,12]

import os
import time
import subprocess
import _pickle as pickle
import sys
from socket import *
import configparser

#---Initializations---#
config = configparser.ConfigParser()
config.read('config.ini')
condition = sys.argv[1]
mousenm = int(config.get(condition,'mousenumber'))
sizemaze = int(config.get(condition,'mazesize'))
mazefile = config.get(condition,'mazefile')
cond = 0
if condition == 'soft':
	cond = 1 

if not cond:
	import math
	from ev3dev.ev3 import *
	ir = UltrasonicSensor('in4')
	left = UltrasonicSensor('in2')
	right = UltrasonicSensor('in3')
	motorR = Motor('outC')
	motorL = Motor('outB')
	gy = GyroSensor('in1')
	orilist = ['left','up','right','down']

#--Hardware functions--#
#Re-caliberate gyro sensor
def gyreset():
    gy.mode = 'GYRO-RATE'
    gy.mode = 'GYRO-G&A'
    while(True):
        ang,rt = gy.rate_and_angle
        if(ang == 0 and rt == 0):
            break
    direc = gy.value()
    return(direc)

#Change the navigating direction as it goes to avoid drift as much as possible
def direchange(lold, rold, direc):
    l = left.value()
    r = right.value()
    #if l - lold > 0 and r - rold < 0 and l + r > 140 and l + r < 180:
    if (l < 75 and l + r > 130 and l <= lold + 1) or (l > 2400):
        direc = direc - 0.2
        lold = l
        rold = r
    #if l - lold < 0 and r - rold > 0 and l + r > 140 and l + r < 180:
    if (r < 75 and l + r > 130 and r <= rold + 1) or (r > 2400):
        direc = direc + 0.2
        lold = l
        rold = r
    return lold, rold, direc

#When finishing a movement, adjust the direction to the navigation direction
def adjust_stable(direc):
    while(True):
        ang,rt = gy.rate_and_angle
        #print(str(r) + ' ' + str(a) + ' ' + str(direc))
        if gy.value() > direc + 1.2:
            if rt == 0:
                motorR.run_direct(duty_cycle_sp=-25)
                motorL.run_direct(duty_cycle_sp=25)
            else:
                motorR.run_direct(duty_cycle_sp=-15)
                motorL.run_direct(duty_cycle_sp=15)
        elif gy.value() < direc - 1.2:
            if rt == 0:
                motorR.run_direct(duty_cycle_sp=25)
                motorL.run_direct(duty_cycle_sp=-25)
            else:
                motorR.run_direct(duty_cycle_sp=15)
                motorL.run_direct(duty_cycle_sp=-15)
        elif gy.value() >= direc - 2 and gy.value() <= direc + 2:
            time.sleep(0.1)
            if rt <= 15 and rt >= -15:
                motorR.stop(stop_action='hold')
                motorL.stop(stop_action='hold')
                break
            continue

def turn_right(direc,ori):
    direc = direc - 90
    ori = ori + 1
    motorL.run_direct(duty_cycle_sp=30)
    motorR.run_direct(duty_cycle_sp=-30)
    while(True):
        ang,rt = gy.rate_and_angle
        if gy.value() <= direc + 15 and gy.value() > direc:
            motorL.run_direct(duty_cycle_sp=20)
            motorR.run_direct(duty_cycle_sp=-20)
        elif gy.value() > direc and rt == 0:
            motorL.run_direct(duty_cycle_sp=25)
            motorR.run_direct(duty_cycle_sp=-25)
        elif gy.value() <= direc:
            motorR.stop(stop_action='hold')
            motorL.stop(stop_action='hold')
            break
    adjust_stable(direc)
    return(direc,ori)

def turn_left(direc,ori):
    ori = ori - 1
    direc = direc + 90
    motorL.run_direct(duty_cycle_sp=-30)
    motorR.run_direct(duty_cycle_sp=30)
    while(True):
        ang,rt = gy.rate_and_angle
        if gy.value() >= direc - 15 and gy.value() < direc:
            motorL.run_direct(duty_cycle_sp=-20)
            motorR.run_direct(duty_cycle_sp=20)
        elif gy.value() < direc and rt == 0:
            motorL.run_direct(duty_cycle_sp=-25)
            motorR.run_direct(duty_cycle_sp=25)
        elif gy.value() >= direc:
            motorR.stop(stop_action='hold')
            motorL.stop(stop_action='hold')
            break
    adjust_stable(direc)
    return(direc,ori)

#turn to the opposite direction, when doing even times of it, reset gyro to make it more accurate
def turn_back(direc, backturnp , ori):
    ori = ori + 2
    if backturnp % 2:
        direc = direc + 180
        motorL.run_direct(duty_cycle_sp=-30)
        motorR.run_direct(duty_cycle_sp=30)
        while(True):
            ang,rt = gy.rate_and_angle
            if gy.value() >= direc - 15 and gy.value() < direc:
                motorL.run_direct(duty_cycle_sp=-20)
                motorR.run_direct(duty_cycle_sp=20)
            elif ang < direc and rt == 0:
                motorL.run_direct(duty_cycle_sp=-25)
                motorR.run_direct(duty_cycle_sp=25)
            elif gy.value() >= direc:
                motorR.stop(stop_action='hold')
                motorL.stop(stop_action='hold')
                break
        adjust_stable(direc)
    else:
        direc = direc - 180
        motorL.run_direct(duty_cycle_sp=30)
        motorR.run_direct(duty_cycle_sp=-30)
        while(True):
            ang,rt = gy.rate_and_angle
            if gy.value() <= direc + 15 and gy.value() > direc:
                motorL.run_direct(duty_cycle_sp=20)
                motorR.run_direct(duty_cycle_sp=-20)
            elif ang > direc and rt == 0:
                motorL.run_direct(duty_cycle_sp=25)
                motorR.run_direct(duty_cycle_sp=-25)
            elif gy.value() <= direc:
                motorR.stop(stop_action='hold')
                motorL.stop(stop_action='hold')
                break
        adjust_stable(direc)
    backturnp = backturnp + 1
    if backturnp % 2 == 0:
        time.sleep(2.8)
        direc = gyreset()
    return(direc, backturnp, ori)

#Ramp down at the end of each move to avoid harming the maze table
def go_straight(direc,xaxis,yaxis,ori):
    startT = time.time()
    refT = startT
    lold = left.value()
    rold = right.value()
    if ori % 4 == 0:
        xaxis = xaxis - 1
    if ori % 4 == 1:
        yaxis = yaxis - 1
    if ori % 4 == 2:
        xaxis = xaxis + 1
    if ori % 4 == 3:
        yaxis = yaxis + 1
    while(True):
        if gy.value() > direc:
            motorR.run_direct(duty_cycle_sp=66)
            motorL.run_direct(duty_cycle_sp=74)
        if gy.value() < direc:
            motorR.run_direct(duty_cycle_sp=74)
            motorL.run_direct(duty_cycle_sp=66)
        if gy.value() == direc:
            motorR.run_direct(duty_cycle_sp=70)
            motorL.run_direct(duty_cycle_sp=70)
        if time.time()- startT > 1.35:
            if gy.value() > direc:
                motorR.run_direct(duty_cycle_sp=38)
                motorL.run_direct(duty_cycle_sp=42)
            if gy.value()< direc:
                motorR.run_direct(duty_cycle_sp=42)
                motorL.run_direct(duty_cycle_sp=38)
            if gy.value() > direc:
                motorR.run_direct(duty_cycle_sp=40)
                motorL.run_direct(duty_cycle_sp=40)
        if time.time()- startT > 1.55:
            motorR.run_direct(duty_cycle_sp=15)
            motorL.run_direct(duty_cycle_sp=15)
        lold, rold, direc = direchange(lold, rold, direc)
        if time.time()- startT > 1.7:
            motorR.stop(stop_action='hold')
            motorL.stop(stop_action='hold')
            adjust_stable(direc)
            return(direc,xaxis,yaxis)

#According to the maze representation table and the readings of the sensors, the current orientation, judge which value is the current grid is in.
def judgegrid(a,l,r,ori):
    if ori % 4 == 0:
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 0
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 3
        if r > 180 and r < 2000 and l < 180 and l > 10  and a < 180 and a > 10:
            return 9
        if r > 180 and r < 2000 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 2
        if r < 180 and r > 10 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 1
        if r < 180 and r > 10 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 5
        if r < 180 and r > 10 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 7
        if r < 180 and r > 10 and l < 180 and l > 10 and a < 180 and a > 10:
            return 13
    if ori % 4 == 1:
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 0
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 1
        if r > 180 and r < 2000 and l < 180 and l > 10  and a < 180 and a > 10:
            return 7
        if r > 180 and r < 2000 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 3
        if r < 180 and r > 10 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 4
        if r < 180 and r > 10 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 6
        if r < 180 and r > 10 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 8
        if r < 180 and r > 10 and l < 180 and l > 10 and a < 180 and a > 10:
            return 12
    if ori % 4 == 2:
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 0
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 4
        if r > 180 and r < 2000 and l < 180 and l > 10  and a < 180 and a > 10:
            return 8
        if r > 180 and r < 2000 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 1
        if r < 180 and r > 10 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 2
        if r < 180 and r > 10 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 5
        if r < 180 and r > 10 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 10
        if r < 180 and r > 10 and l < 180 and l > 10 and a < 180 and a > 10:
            return 14
    if ori % 4 == 3:
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 0
        if r > 180 and r < 2000 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 2
        if r > 180 and r < 2000 and l < 180 and l > 10  and a < 180 and a > 10:
            return 10
        if r > 180 and r < 2000 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 4
        if r < 180 and r > 10 and l > 180 and l < 2000 and a > 180 and a < 2000:
            return 3
        if r < 180 and r > 10 and l < 180 and l > 10 and a > 180 and a < 2000:
            return 6
        if r < 180 and r > 10 and l > 180 and l < 2000 and a < 180 and a > 10:
            return 9
        if r < 180 and r > 10 and l < 180 and l > 10 and a < 180 and a > 10:
            return 11

#--End of Hardware functions--#

#Getting the ID of each agent, different implementations for different situations
def getdit(myip,cond):
	if cond:
		dit = int(str(myip.split()[2]).split(":")[2][0])
	else:
		dit = int(str(myip.split()[0]).split(".")[3][0]) - 2
	return dit

#Initialize the initial coordinations, hardware side since it cannot read where it is, just manually put in the numbers and orientations
def getInitxy(cond,mousenm):
	if cond:
		xyfile = []
		corexys = []
		corexy = []
		xaxis = []
		yaxis = []
		xpos = []
		ypos = []
		for num in range(mousenm):
			xyfile.append(open("../n"+str(num+1)+".xy", 'r'))
			corexys.append(xyfile[num].read())
			corexy.append([float(s) for s in corexys[num].split()])
			xaxis.append(round((corexy[num][0]-42)/72))
			yaxis.append(round((corexy[num][1]-25)/48))
			xpos.append(xaxis[num]*72+42)
			ypos.append(yaxis[num]*48+25)
			ori = [0]*mousenm
	else:
		xaxis = [7,0]
		yaxis = [7,0]
		ypos = [0,0]
		xpos = [0,0]
		ori = [0,3]
		
	return list(map(int, xaxis)), list(map(int, yaxis)), list(map(int, xpos)), list(map(int, ypos)), ori

'''
#not using this function for checking neighbors since it runs pretty slow.
def checkNeib():
	k=os.popen("ip route | awk -F\" \" '{ if($3 ==\"eth0\" && $1!=\"10.0.0.0/24\") print $1 }'|sort -R", "r")
	neibors = k.read().count('\n')
	return neibors
'''	

#Check if the grid is invisited
def inVisited(visited, x, y):
	for t in visited:
		if(x==t[0] and y==t[1]):
			return 0
	return 1

#Check if it's going to be a collision
def collision(xin,yin,mouse,mousenm):
	ansco = False
	for n in range(mousenm):
		ansco = (ansco or [xin,yin] == [mouse[n].x, mouse[n].y])
	return ansco

#Reversing to the steps indicated
def reverse(path1,mouse,ipgroup,cond):
	last = path1.pop()
	if(last=="up"):
		mouse.backward(ipgroup,cond)
	elif(last=="down"):
		mouse.forward(ipgroup,cond)
	elif(last=="right"):
		mouse.left(ipgroup,cond)
	elif(last=="left"):
		mouse.right(ipgroup,cond)
		
#checking if the agent's task is finished
def checkFinish(mouse,xaxis,yaxis,dit,mousenm,sizemaze):
	anslocal = False
	# 4 directions out of border check
	ansln = False
	ansls = False
	ansle = False
	anslw = False
	for n in range(mousenm):
		anslocal = (anslocal or not mouse[n].mapm[yaxis[dit-1]][xaxis[dit-1]] == sizemaze)
	if yaxis[dit-1] < sizemaze-1:
		for n in range(mousenm):
			ansls = (ansls or not mouse[n].mapm[yaxis[dit-1]+1][xaxis[dit-1]] == sizemaze)
	else:
		ansls = True
	if xaxis[dit-1] < sizemaze-1:
		for n in range(mousenm):
			ansle = (ansle or not mouse[n].mapm[yaxis[dit-1]][xaxis[dit-1]+1] == sizemaze)
	else:
		ansle = True
	if yaxis[dit-1] > 0:
		for n in range(mousenm):
			ansln = (ansln or not mouse[n].mapm[yaxis[dit-1]-1][xaxis[dit-1]] == sizemaze)
	else:
		ansln = True
	if xaxis[dit-1] > 0:
		for n in range(mousenm):
			anslw = (anslw or not mouse[n].mapm[yaxis[dit-1]][xaxis[dit-1]-1] == sizemaze)
	else:
		anslw = True
	return (anslocal and ansln and ansls and ansle and anslw)

#Check if the agent can go to the direction
def cangoLeft(m,leftlist):
	return m.mapm[m.y][m.x] in leftlist

def cangoRight(m,rightlist):
	return m.mapm[m.y][m.x] in rightlist

def cangoUp(m,uplist):
	return m.mapm[m.y][m.x] in uplist

def cangoDown(m,downlist):
	return m.mapm[m.y][m.x] in downlist

#DFS search including collisions
def depthFirst(mouse,mouselist,visited,ipgroup,cond,mousenm):
	if(cangoRight(mouse,rightlist) and inVisited(visited,mouse.x+1,mouse.y) and not collision(mouse.x+1,mouse.y,mouselist,mousenm)):				
		mouse.right(ipgroup,cond)
		mouse.path.append("right")
	elif(cangoDown(mouse,downlist) and inVisited(visited,mouse.x,mouse.y+1) and not collision(mouse.x,mouse.y+1,mouselist,mousenm)):	
		mouse.backward(ipgroup,cond)
		mouse.path.append("down")
	elif (cangoLeft(mouse,leftlist) and inVisited(visited,mouse.x-1,mouse.y) and not collision(mouse.x-1,mouse.y,mouselist,mousenm)):	
		mouse.left(ipgroup,cond)
		mouse.path.append("left")
	elif(cangoUp(mouse,uplist) and inVisited(visited,mouse.x,mouse.y-1) and not collision(mouse.x,mouse.y-1,mouselist,mousenm)):	
		mouse.forward(ipgroup,cond)
		mouse.path.append("up")
	elif(len(mouse.path) > 0):
		reverse(mouse.path,mouse,ipgroup,cond)
	elif(cangoRight(mouse,rightlist) and not collision(mouse.x+1,mouse.y,mouselist,mousenm)):			
		mouse.right(ipgroup,cond)
		mouse.path.append("right")
	elif(cangoDown(mouse,downlist) and not collision(mouse.x,mouse.y+1,mouselist,mousenm)):		
		mouse.backward(ipgroup,cond)
		mouse.path.append("down")
	elif (cangoLeft(mouse,leftlist) and not collision(mouse.x-1,mouse.y,mouselist,mousenm)):		
		mouse.left(ipgroup,cond)
		mouse.path.append("left")
	elif(cangoUp(mouse,uplist) and not collision(mouse.x,mouse.y-1,mouselist,mousenm)):	
		mouse.forward(ipgroup,cond)
		mouse.path.append("up")
		
#Software maze updating to the agent
def supdateMaze(mouse,arr):
	mouse.mapm[mouse.y][mouse.x]=arr[mouse.y][mouse.x]

#Hardware maze updating to the agent
def hupdateMaze(mouse,ir,left,right):
	mouse.mapm[mouse.y][mouse.x]=judgegrid(ir,left,right,mouse.ori)
	print(mouse.mapm[mouse.y][mouse.x])

#Class of Mouse
#Uncomment the comments and comment os sentences for getting animation effect, but will be slow.
class Mouse:
	xpos = 0
	ypos = 0
	x = 0
	y = 0
	idM = 0
	strx = 0
	stry = 0
	path=[]
	mapm = []
	ori = 0
	backturnp = 0
	direc = 0
	def __init__(self, xpos, ypos, xaxis, yaxis, idM, sizemaze, ori):      
		self.xpos = xpos
		self.ypos = ypos
		self.x = xaxis
		self.y = yaxis
		self.ori = ori
		self.idM = idM
		self.strx= xpos
		self.stry= ypos
		self.mapm= []
		for num in range(0,sizemaze):
			map1=[]
			for num1 in range(0,sizemaze):
				map1.append(16)
			self.mapm.append(map1)

	def forward(self,ipgroup,cond):
		if cond:
			oldpos = self.ypos
			self.ypos = self.ypos - 48;
			self.y = self.y - 1;
			#for i in range(oldpos,self.ypos,-4):	
			#	os.system("coresendmsg -a 10.0.0.254 node number="+str(self.idM)+" xpos="+str(self.xpos)+" ypos="+str(i))
			#	time.sleep(0.002)
			os.system("coresendmsg -a " + ipgroup + ".254 node number="+str(self.idM)+" xpos="+str(self.xpos)+" ypos="+str(self.ypos))
		else:
			ir = UltrasonicSensor('in4')
			left = UltrasonicSensor('in2')
			right = UltrasonicSensor('in3')
			motorR = Motor('outC')
			motorL = Motor('outB')
			gy = GyroSensor('in1')
			if self.ori % 4 == 0:
				self.direc, self.ori = turn_right(self.direc, self.ori) 
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 1:
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 2:
				self.direc, self.ori = turn_left(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 3:
				self.direc, self.backturnp, self.ori = turn_back(self.direc, self.backturnp, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)

	def backward(self,ipgroup,cond):
		if cond:
			oldpos = self.ypos
			self.ypos = self.ypos + 48;
			self.y = self.y + 1;
			#for i in range(oldpos,self.ypos,4):
			#	os.system("coresendmsg -a 10.0.0.254 node number="+str(self.idM)+" xpos="+str(self.xpos)+" ypos="+str(i))
			#	time.sleep(0.002)
			os.system("coresendmsg -a " + ipgroup + ".254 node number="+str(self.idM)+" xpos="+str(self.xpos)+" ypos="+str(self.ypos))
		else:
			ir = UltrasonicSensor('in4')
			left = UltrasonicSensor('in2')
			right = UltrasonicSensor('in3')
			motorR = Motor('outC')
			motorL = Motor('outB')
			gy = GyroSensor('in1')
			if self.ori % 4 == 0:
				self.direc, self.ori = turn_left(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 1:
				self.direc, self.backturnp, self.ori = turn_back(self.direc, self.backturnp, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 2:
				self.direc, self.ori = turn_right(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 3:
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
    
	def right(self,ipgroup,cond):
		if cond:
			oldpos = self.xpos
			self.xpos = self.xpos + 72;
			self.x = self.x + 1;
			#for i in range(oldpos,self.xpos,4):
			#	os.system("coresendmsg -a 10.0.0.254 node number="+str(self.idM)+" xpos="+str(i)+" ypos="+str(self.ypos))
			#	time.sleep(0.001)
			os.system("coresendmsg -a " + ipgroup + ".254 node number="+str(self.idM)+" xpos="+str(self.xpos)+" ypos="+str(self.ypos))
		else:
			ir = UltrasonicSensor('in4')
			left = UltrasonicSensor('in2')
			right = UltrasonicSensor('in3')
			motorR = Motor('outC')
			motorL = Motor('outB')
			gy = GyroSensor('in1')
			if self.ori % 4 == 0:
				self.direc, self.backturnp, self.ori = turn_back(self.direc, self.backturnp, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 1:
				self.direc, self.ori = turn_right(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 2:
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 3:
				self.direc, self.ori = turn_left(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)  

	def left(self,ipgroup,cond):
		if cond:
			oldpos = self.xpos
			self.xpos = self.xpos - 72;
			self.x = self.x - 1;
			#for i in range(oldpos,self.xpos,-4):
			#	os.system("coresendmsg -a 10.0.0.254 node number="+str(self.idM)+" xpos="+str(i)+" ypos="+str(self.ypos))
			#	time.sleep(0.001)
			os.system("coresendmsg -a " + ipgroup + ".254 node number="+str(self.idM)+" xpos="+str(self.xpos)+" ypos="+str(self.ypos))
		else:
			ir = UltrasonicSensor('in4')
			left = UltrasonicSensor('in2')
			right = UltrasonicSensor('in3')
			motorR = Motor('outC')
			motorL = Motor('outB')
			gy = GyroSensor('in1')
			if self.ori % 4 == 0:
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 1:
				self.direc, self.ori = turn_left(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 2:
				self.direc, self.backturnp, self.ori = turn_back(self.direc, self.backturnp, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)
			elif self.ori % 4 == 3:
				self.direc, self.ori = turn_right(self.direc, self.ori)
				self.direc, self.x ,self.y = go_straight(self.direc, self.x ,self.y, self.ori)

#Reading maze, if it's hardware, we don't provide the maze
def readmaze(cond,mazefile):
	if cond:
		mfile = open(mazefile, 'r')
		arra = []
		for line in mfile.readlines():
			arr1 = []
			for c in line:
				if(c.isspace() and (c!="\n")):
				    arr1.append(1)
				elif(c =="+" or c == "."):
				    arr1.append(9)
				elif(c == "-"):
				    arr1.append(4)
				elif(c == "|"):
				    arr1.append(7)
			arra.append(arr1)
		arr = []
		for y in range(len(arra)):
			if y % 2 == 1:
				mazeforead1 = []
				for x in range(len(arra)):
					if arra[y][x] == 1:
						if arra[y-1][x] == 1 and arra[y][x-1] == 1 and arra[y+1][x] == 1 and arra[y][x+1] == 1:
							mazeforead1.append(0)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 1 and arra[y+1][x] == 1 and arra[y][x+1] == 1:
							mazeforead1.append(1)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 1 and arra[y+1][x] == 4 and arra[y][x+1] == 1:
							mazeforead1.append(2)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 7 and arra[y+1][x] == 1 and arra[y][x+1] == 1:
							mazeforead1.append(3)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 1 and arra[y+1][x] == 1 and arra[y][x+1] == 7:
							mazeforead1.append(4)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 1 and arra[y+1][x] == 4 and arra[y][x+1] == 1:
							mazeforead1.append(5)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 7 and arra[y+1][x] == 1 and arra[y][x+1] == 7:
							mazeforead1.append(6)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 7 and arra[y+1][x] == 1 and arra[y][x+1] == 1:
							mazeforead1.append(7)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 1 and arra[y+1][x] == 1 and arra[y][x+1] == 7:
							mazeforead1.append(8)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 7 and arra[y+1][x] == 4 and arra[y][x+1] == 1:
							mazeforead1.append(9)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 1 and arra[y+1][x] == 4 and arra[y][x+1] == 7:
							mazeforead1.append(10)
						elif arra[y-1][x] == 1 and arra[y][x-1] == 7 and arra[y+1][x] == 4 and arra[y][x+1] == 7:
							mazeforead1.append(11)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 7 and arra[y+1][x] == 1 and arra[y][x+1] == 7:
							mazeforead1.append(12)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 7 and arra[y+1][x] == 4 and arra[y][x+1] == 1:
							mazeforead1.append(13)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 1 and arra[y+1][x] == 4 and arra[y][x+1] == 7:
							mazeforead1.append(14)
						elif arra[y-1][x] == 4 and arra[y][x-1] == 7 and arra[y+1][x] == 4 and arra[y][x+1] == 7:
							mazeforead1.append(15)
				arr.append(mazeforead1)
	else:
		arr = []
	return arr
	

#Initialization of mouse
def initMouse(mousenm,xpos,ypos,xaxis,yaxis,sizemaze,ori):
	mouse = []
	for n in range(mousenm):
		mouse.append(Mouse(xpos[n], ypos[n], xaxis[n], yaxis[n], n+1, sizemaze,ori[n]))
	return mouse
