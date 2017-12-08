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
import DDFSfunc
import configparser

#---Initializations---#
config = configparser.ConfigParser()
config.read('./config.ini')
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
	DDFSfunc.gyreset()



#---Port Specification & Communication---#
MYPORT = 50000
myip = subprocess.check_output(["hostname", "-I"])
print(myip)
time.sleep(3)
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.settimeout(4.0)

ipgroup = str(myip.split()[cond])[2:-3]

#---Maze Reading---#
#Please change the maze file you want to load for this parameter.
arr = DDFSfunc.readmaze(cond,mazefile)

#---Mouse Initialization---#
#Knowing the ID of itself.
dit = DDFSfunc.getdit(myip,cond)
xaxis,yaxis,xpos,ypos,ori =  DDFSfunc.getInitxy(cond,mousenm)

mouse = DDFSfunc.initMouse(mousenm,xpos,ypos,xaxis,yaxis,sizemaze,ori)

visited=[]
visited.append([mouse[dit-1].x,mouse[dit-1].y])
itnum = 0

#---Main Program---#
while(True):
	#---Sending & Receiving Data---#
	if not itnum == 0:
		s.sendto(dss, (ipgroup +'.255', MYPORT))
		odss = ['' for j in range(mousenm)]
		for odssn in odss:
			try:
				odssn, addr = s.recvfrom(20000)
				data = pickle.loads(odssn)
				dfrom = data[2]
				print('get '+str(dfrom))
				visited.append(data[0])
				mouse[dfrom-1].x = data[1][0]
				mouse[dfrom-1].y = data[1][1]
				mouse[dfrom-1].mapm = data[1][2]
				mouse[dfrom-1].xpos = data[1][3]
				mouse[dfrom-1].ypos = data[1][4]
			except timeout:
				pass
			
	#---Checking Local Finish---#
	if [mouse[dit-1].x,mouse[dit-1].y] == [xaxis[dit-1],yaxis[dit-1]] and DDFSfunc.checkFinish(mouse,xaxis,yaxis,dit,mousenm,sizemaze) and not itnum == 0:
		time.sleep(0.08)
		continue
	if cond == 0 and itnum == 0:
		mouse[dit-1].direc, mouse[dit-1].x ,mouse[dit-1].y = DDFSfunc.go_straight(mouse[dit-1].direc, mouse[dit-1].x ,mouse[dit-1].y, mouse[dit-1].ori)
		
	DDFSfunc.depthFirst(mouse[dit-1],mouse,visited,ipgroup,cond,mousenm)

	if cond:
		DDFSfunc.supdateMaze(mouse[dit-1],arr)
	else:
		time.sleep(1)
		DDFSfunc.hupdateMaze(mouse[dit-1],ir.value(),left.value(),right.value())

	visited.append([mouse[dit-1].x,mouse[dit-1].y])
	#---Preparing Data for Sending---#
	datas = []
	ms = []
	ms.append(mouse[dit-1].x)
	ms.append(mouse[dit-1].y)
	ms.append(mouse[dit-1].mapm)
	ms.append(mouse[dit-1].xpos)
	ms.append(mouse[dit-1].ypos)
	datas.append([mouse[dit-1].x,mouse[dit-1].y])
	datas.append(ms)
	datas.append(dit)
	dss = pickle.dumps(datas)
	val = ''
	itnum = itnum + 1
	time.sleep(0.1)



