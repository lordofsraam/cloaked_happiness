import sys, os, subprocess
import xml.etree.ElementTree as ET
from net_scan_structs import Display_Types
from net_scan_host import Host

def _print(string,do=Display_Types.CLI):
	if do  == Display_Types.CLI:
		print string
	elif do  == Display_Types.NCURSES:
		pass
	elif do == Display_Types.GRAPHIC:
		pass

def scan(hosts,do=Display_Types.CLI):
	devnull = open('/dev/null', 'w')
	_print("Scanning...",do)
	subprocess.call("nmap -sn "+hosts+" -oX res.xml",shell=True,stdout=devnull)
	_print("Done.",do)
	res = ET.parse('res.xml')
	_print("File parsed.",do)
	root = res.getroot()
	for child in filter(lambda c: c.tag == 'host', root):
		_print(Host(child).summary,do)
	
