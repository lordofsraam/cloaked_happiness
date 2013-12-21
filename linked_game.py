#! /usr/bin/python

import os, sys, curses, locale, random, math

mainscr = None

global_index = 0

arr = []
class Node:
	def __init__(self, data):
		self.data = data
		self.next = None
		self.prev = None

def on_key_down(key):
	global global_index
	if key == ord('Q'):
		curses.endwin()
		exit()
	elif key == 260: #Left arrow
		mainscr.clear()
		global_index += 1
		draw_square(global_index%16)
		mainscr.refresh()
	elif key == 261: #Right arrow
		mainscr.clear()
		if (global_index - 1) < 0: global_index = (16*16)-1
		else: global_index -= 1
		draw_square(global_index%16)
		mainscr.refresh()

def draw_square(start_index=0):
	global arr
	win_y,win_x = mainscr.getmaxyx()
	str_len = 5
	draw_posY = (win_y/2) - 5
	draw_posX = (win_x/2) - int(str_len*3)

	curr = arr[start_index]
	index = 0

	#for i in xrange(0,len(arr)*3, 3):
		#mainscr.addstr(1,1+i,str(arr[i/3].data))

	for i in xrange(0,(str_len*5),str_len):
		mainscr.addstr(draw_posY,draw_posX+i,"["+str(curr.data)+"]")
		curr = curr.next

	for i in xrange(0,(2*3),2):
		mainscr.addstr(draw_posY+i+2,draw_posX+(str_len*4),"["+str(curr.data)+"]")
		curr = curr.next

	for i in xrange(0,(str_len*5),str_len):
		mainscr.addstr(draw_posY+8,draw_posX+(str_len*4)-i,"["+str(curr.data)+"]")
		curr = curr.next

	for i in xrange(0,(2*3),2):
		mainscr.addstr(draw_posY-i+6,draw_posX,"["+str(curr.data)+"]")
		curr = curr.next
	


if __name__ == "__main__":
	global mainscr
	global arr
	#Linking
	for i in xrange(16): arr.append(Node(random.randint(10,99)))
	for n in xrange(15): arr[n].next = arr[n+1]
	for n in xrange(1,16): arr[n].prev = arr[n-1]
	#Close the circle
	arr[len(arr)-1].next = arr[0]
	arr[0].prev = arr[len(arr)-1]

	locale.setlocale(locale.LC_ALL,"")
	mainscr = curses.initscr()
	mainscr.nodelay(True)
	mainscr.keypad(1)
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)

	draw_square(global_index)

	while 1:
		on_key_down(mainscr.getch())