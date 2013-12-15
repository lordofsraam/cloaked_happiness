#!/usr/bin/python

import sys, os, argparse, curses, xml, locale, math

from time import sleep
from multiprocessing import Process

from net_scan_scanner import scan
from net_scan_structs import Display_Types
from net_scan_host import Host, DSHost

import sys, os, subprocess
import xml.etree.ElementTree as ET

file_available = False
need_clear = False
filter_state = "OFF"

def _print(string):
	global mainscr
	if args.display_option  == Display_Types.CLI:
		print string
	elif args.display_option  == Display_Types.NCURSES:
		mainscr.addstr(mainscr.getmaxyx()[0]-1,mainscr.getmaxyx()[1]/2," "*((mainscr.getmaxyx()[1]/2)-1))
		mainscr.addstr(mainscr.getmaxyx()[0]-1,mainscr.getmaxyx()[1]/2,">"+string)
		refresh_all()
	elif args.display_option == Display_Types.GRAPHIC:
		pass

def refresh_all():
	global mainscr
	global dscanscr
	if args.display_option  == Display_Types.NCURSES:
		mainscr.refresh()
		if dscanscr != None:
			dscanscr.redrawwin()
			dscanscr.overwrite(mainscr)
			dscanscr.refresh()

hosts_res = []
ip_width = 24
def scan(hosts):
	global need_clear
	global filter_state
	global ip_width
	if file_available:
		try:
			res = ET.parse('res.xml')
			_print("File parsed.")
			root = res.getroot()
			global hosts_res
			hosts_res = []
			for child in filter(lambda c: c.tag == 'host', root):
				hosts_res.append(Host(child))
			if args.display_option == Display_Types.CLI:
				for c in hosts_res:
					print c.summary
			# elif args.display_option == Display_Types.NCURSES:
			# 	count = 0
			# 	inc = 0
			# 	max_in_x = (mainscr.getmaxyx()[1]/ip_width)
			# 	max_in_y = (mainscr.getmaxyx()[0]/max_in_x)
			# 	for c in hosts_res:
			# 		if count/max_in_y < max_in_y:
			# 			index_str = "("+("%3d"%count).replace(" ","0")+")"
			# 			if filter_state == "UP":
			# 				if c.state == 'up':
			# 					mainscr.addstr(inc/max_in_x,(inc%max_in_x)*ip_width,(index_str+" "+c.summary).encode('utf-8'))
			# 					inc += 1
			# 			elif filter_state == "DOWN":
			# 				if c.state != 'up':
			# 					mainscr.addstr(inc/max_in_x,(inc%max_in_x)*ip_width,(index_str+" "+c.summary).encode('utf-8'))
			# 					inc += 1
			# 			else:
			# 				mainscr.addstr(count/max_in_x,(count%max_in_x)*ip_width,(index_str+" "+c.summary).encode('utf-8'))
			# 		else:
			# 			break
			# 		count += 1
			# 	if need_clear:
			# 		mainscr.clear()
			# 		need_clear = False
			# 	mainscr.addstr(mainscr.getmaxyx()[0]-1,0,":"+input_str)
			# 	refresh_all()
			redraw_hosts()
		except xml.etree.ElementTree.ParseError:
			_print("Waiting for file.")
	else:
		_print("File not available.")

def redraw_hosts():
	global ip_width
	global need_clear
	global filter_state
	if args.display_option  == Display_Types.NCURSES:
		count = 0
		inc = 0
		max_in_x = (mainscr.getmaxyx()[1]/ip_width)
		max_in_y = (mainscr.getmaxyx()[0]/max_in_x)
		for c in hosts_res:
			if count/max_in_y < max_in_y:
				index_str = "("+("%3d"%count).replace(" ","0")+")"
				if filter_state == "UP":
					if c.state == 'up':
						mainscr.addstr(inc/max_in_x,(inc%max_in_x)*ip_width,(index_str+" "+c.summary).encode('utf-8'))
						inc += 1
				elif filter_state == "DOWN":
					if c.state != 'up':
						mainscr.addstr(inc/max_in_x,(inc%max_in_x)*ip_width,(index_str+" "+c.summary).encode('utf-8'))
						inc += 1
				else:
					mainscr.addstr(count/max_in_x,(count%max_in_x)*ip_width,(index_str+" "+c.summary).encode('utf-8'))
			else:
				break
			count += 1
		if need_clear:
			mainscr.clear()
			need_clear = False
		mainscr.addstr(mainscr.getmaxyx()[0]-1,0,":"+input_str)
		refresh_all()

dscanscr = None
def dscan(host):
	global dscanscr
	dscanscr = curses.newwin(mainscr.getmaxyx()[0]/2,mainscr.getmaxyx()[1]/2,mainscr.getmaxyx()[0]/4,mainscr.getmaxyx()[1]/4)
	dscanscr.border()
	dscanscr.addstr(0,(dscanscr.getmaxyx()[1]/2)-(len(host.addr)/2),host.addr)
	dscanscr.addstr(1,1,"MAC: "+host.mac)
	dscanscr.addstr(2,1,"Vendor: "+host.vendor)
	dscanscr.addstr(3,1,"Loading more info...")
	dscanscr.refresh()
	subprocess.call("sudo nmap -v "+host.addr+" -oX dsres.xml",shell=True,stdout=devnull)
	res = ET.parse('dsres.xml')
	root = res.getroot()
	host_res = DSHost(filter(lambda c: c.tag == 'host', root)[0])
	dscanscr.addstr(3,1," "*(dscanscr.getmaxyx()[1]-2))
	dscanscr.addstr(3,1,"Number of open ports: "+str(host_res.num_of_ports))
	if host_res.num_of_ports > 0:
		i = 0
		while i < host_res.num_of_ports and i < (dscanscr.getmaxyx()[1]-5):
			dscanscr.addstr(4+i,1,"Port "+host_res.ports[i].number+": "+host_res.ports[i].protocol)
			i += 1

def cmd_proc(commands):
	global bg_proc
	global dscanscr
	global need_clear
	global filter_state
	commands_list = commands.split(" ")
	if commands.upper() == "QUIT":
		curses.endwin()
		bg_proc.terminate()
		exit()
	elif commands.upper() == "FLASH":
		curses.flash()
	elif commands_list[0].upper() == "DSCAN" and len(commands_list) > 1:
		dscan(hosts_res[int(commands_list[1])])
	elif commands.upper() == "CLEAR":
		dscanscr = None
		need_clear = True
		refresh_all()
	elif commands_list[0].upper() == "FILTER" and len(commands_list) > 1:
		need_clear = True
		if commands_list[1].upper() == "UP":
			filter_state = "UP"
		elif commands_list[1].upper() == "DOWN":
			filter_state = "DOWN"
		elif commands_list[1].upper() == "NONE" or commands_list[1].upper() == "OFF":
			filter_state = "OFF"
		redraw_hosts()
	elif commands.upper() == "REDRAW":
		redraw_hosts()

devnull = open('/dev/null', 'w')
def nmap_loop():
	while 1:
		file_available = False
		subprocess.call("nmap -n -v -sn "+args.target+" -oX res.xml",shell=True,stdout=devnull)
		file_available = True
		sleep(1)

input_str = ""
def on_key_down(key):
	global input_str

	def refresh():
		global input_str
		mainscr.addstr(mainscr.getmaxyx()[0]-1,0," "*(mainscr.getmaxyx()[1]/2))
		mainscr.addstr(mainscr.getmaxyx()[0]-1,0,":"+input_str)
		refresh_all()

	if key == ord('Q'):
		curses.endwin()
		bg_proc.terminate()
		exit()
	elif key > 0 and key < 256:
		if key != 10:
			input_str += chr(key)
		else:
			cmd_proc(input_str)
			input_str = ""
		refresh()
	elif key == 259:
		input_str += "up"
		refresh()
	elif key == curses.KEY_BACKSPACE:
		input_str = input_str[:-1]
		refresh()

parser = argparse.ArgumentParser(description='Network scanner.')
parser.add_argument('-d','--display', nargs='?', dest='display_option',help='How the output should be displayed')
parser.add_argument('-t','--target', nargs='?', dest='target',help='Target network',required=True)

args = parser.parse_args()

mainscr = None

if os.geteuid() != 0:
	print "Need root for deep scans."
	exit()

if args.display_option == Display_Types.NCURSES:
	locale.setlocale(locale.LC_ALL,"")
	mainscr = curses.initscr()
	mainscr.nodelay(True)
	mainscr.keypad(1)
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	_print("Loading...")
	file_available = False
	subprocess.call("nmap -n -v -sn "+args.target+" -oX res.xml",shell=True,stdout=devnull)
	file_available = True
elif args.display_option == Display_Types.CLI:
	print 'Output will be display in CLI'
else:
	print 'No display type specified. Will use CLI'
	args.display_option = Display_Types.CLI

bg_proc = Process(target=nmap_loop)

try:
	if args.display_option == Display_Types.NCURSES:
		bg_proc.start()
		while 1:
			scan(args.target)
			on_key_down(mainscr.getch())
	elif args.display_option == Display_Types.CLI:
		_print("Scanning...")
		subprocess.call("nmap -n -v -sn "+args.target+" -oX res.xml",shell=True,stdout=devnull)
		file_available = True
		scan(args.target)
except KeyboardInterrupt:
	curses.endwin()
	exit()