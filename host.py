#!/usr/bin/env python3

#Author: Yang Shi

import os
import time
import _pickle as pickle
MYPORT = 50000
import sys
from socket import *
from tkinter import *


s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

window0 = Tk()

def softhard(condition):
	if condition == 'soft':
		cond = 1
	elif condition == 'hard':
		cond = 0
	else:
		raise Exception('Invalid argument')
	return cond

cond = softhard(sys.argv[1])
if cond:
	mousenm = 4
	sizemaze = 16
	window0.geometry('400x400+1400+500')
else:
	mousenm = 2
	sizemaze = 8


canvas0 = Canvas(window0, width=400, height=400)
canvas0.pack()
width=400
height=400
side = width / sizemaze

def mapsnum(mousenm,row,col,nm):
	answer = False
	for n in range(mousenm):
		answer = answer or maps[n][row][col] == nm
	return(answer)

def updateCanvas(xlist, ylist, maps, visited):
	colorlist = ['yellow', 'blue', 'magenta', 'green']
	combArr = []
	for num in range(sizemaze):
		comb=[]
		for num1 in range(sizemaze):
			comb.append(0)
		combArr.append(comb)	
	for x in visited:
		combArr[x[1]][x[0]] = 1
	for row in range(sizemaze):
		for col in range(sizemaze):
			x = col * side
			y = row * side
			if(row==ylist[0] and col==xlist[0]):
				drawSquare(canvas0, x+2, y+2, side-4, 'yellow')
			elif(row==ylist[1] and col==xlist[1]):
				drawSquare(canvas0, x+2, y+2, side-4, 'blue')
			elif(mapsnum(mousenm,row,col,0)):
				drawSquare(canvas0, x, y, side, 'white0')
			elif(mapsnum(mousenm,row,col,1)):
				drawSquare(canvas0, x, y, side, 'white1')
			elif(mapsnum(mousenm,row,col,2)):
				drawSquare(canvas0, x, y, side, 'white2')
			elif(mapsnum(mousenm,row,col,3)):
				drawSquare(canvas0, x, y, side, 'white3')
			elif(mapsnum(mousenm,row,col,4)):
				drawSquare(canvas0, x, y, side, 'white4')
			elif(mapsnum(mousenm,row,col,5)):
				drawSquare(canvas0, x, y, side, 'white5')
			elif(mapsnum(mousenm,row,col,6)):
				drawSquare(canvas0, x, y, side, 'white6')
			elif(mapsnum(mousenm,row,col,7)):
				drawSquare(canvas0, x, y, side, 'white7')
			elif(mapsnum(mousenm,row,col,8)):
				drawSquare(canvas0, x, y, side, 'white8')
			elif(mapsnum(mousenm,row,col,9)):
				drawSquare(canvas0, x, y, side, 'white9')
			elif(mapsnum(mousenm,row,col,10)):
				drawSquare(canvas0, x, y, side, 'white10')
			elif(mapsnum(mousenm,row,col,11)):
				drawSquare(canvas0, x, y, side, 'white11')
			elif(mapsnum(mousenm,row,col,12)):
				drawSquare(canvas0, x, y, side, 'white12')
			elif(mapsnum(mousenm,row,col,13)):
				drawSquare(canvas0, x, y, side, 'white13')
			elif(mapsnum(mousenm,row,col,14)):
				drawSquare(canvas0, x, y, side, 'white14')
			elif(mapsnum(mousenm,row,col,15)):
				drawSquare(canvas0, x, y, side, 'white15')
			else:
				drawSquare(canvas0, x+1, y+1, side-2, 'red')
			if(cond):
				if(row==ylist[2] and col==xlist[2]):
					drawSquare(canvas0, x+2, y+2, side-4, 'magenta')
				if(row==ylist[3] and col==xlist[3]):
					drawSquare(canvas0, x+2, y+2, side-4, 'green')

	canvas0.update()


	return combArr

def drawSquare(canvas, x, y, side, color):
	if(color=='red'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill=color,outline='black')
	elif(color=='yellow'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill=color,outline='white')
	elif(color=='magenta'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill=color,outline='white')
	elif(color=='green'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill=color,outline='white')
	elif(color=='blue'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill=color,outline='white')
	elif(color == 'white0'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
	elif(color == 'white1'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
	elif(color == 'white2'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
	elif(color == 'white3'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
	elif(color == 'white4'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white5'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
	elif(color == 'white6'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white7'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
	elif(color == 'white8'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white9'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
	elif(color == 'white10'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white11'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white12'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white13'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
	elif(color == 'white14'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	elif(color == 'white15'):
		id = canvas.create_rectangle(x, y, x + side, y + side, fill='white',outline='white')
		id = canvas.create_line(x, y, x + side, y, fill='black',width=3)
		id = canvas.create_line(x, y + side, x + side, y + side, fill='black',width=3)
		id = canvas.create_line(x, y, x, y + side, fill='black',width=3)
		id = canvas.create_line(x + side, y, x + side, y + side, fill='black',width=3)
	return id
odss = ['' for j in range(mousenm)]
m = ['' for j in range(mousenm)]
x = ['' for j in range(mousenm)]
y = ['' for j in range(mousenm)]
maps = ['' for j in range(mousenm)]
visited = []
while(True):
	for odssn in odss:
		odssn, addr = s.recvfrom(20000)
		data = pickle.loads(odssn)
		dfrom = data[2]
		print('get '+str(dfrom))
		visited.append(data[0])
		m[dfrom-1] = data[1]
		x[dfrom-1] = m[dfrom-1][0]
		y[dfrom-1] = m[dfrom-1][1]
		maps[dfrom-1] = m[dfrom-1][2]
	updateCanvas(x, y, maps, visited)

