# -*- coding: utf-8 -*-

from HackerPrint import hackerPrint,hackerPrintErr
import argparse
import sqlite3
import os
import time


banner = r"""
___________    .__        __________                      
\__    ___/___ |  |   ____\______   \_____ _______  ______
  |    |_/ __ \|  | _/ __ \|     ___/\__  \\_  __ \/  ___/
  |    |\  ___/|  |_\  ___/|    |     / __ \|  | \/\___ \ 
  |____| \___  >____/\___  >____|    (____  /__|  /____  >
             \/          \/               \/           \/ 
Version: %s
Programador: %s
Github: https://github.com/nicotrial

Usage: python teleparser.py -h (for help)
""" % ('0.1','Nicotrial')

def printBanner():
	hackerPrint(banner,"HEAVY",True,0.01)
	hackerPrint("\n[-] Developed at UAH","ERROR", True)
	hackerPrintErr("\n[+] AUTHORS : Nicolas Logghe \n","ERROR", True)


def argsParsing():
	parser = argparse.ArgumentParser(description='Extract data from telegram app')
	parser.add_argument('-f',action='store'		,dest='path'		,required=False, help='Path of db file')
	parser.add_argument('-ex',action='store_true',dest='extract'		,required=False, help='Autoextract Telegram app from phone')
	parser.add_argument('-b',action='store_true',dest='banner'		,required=False, help='Do not show Banner')
	args = parser.parse_args()
	return args

def extractApp():
	hackerPrint("[-] Extracting telegram app data from phone\n","GOOD", True)
	os.system("""./Tools/platform-tools/adb""")
	#os.system("""./Tools/platform-tools/adb reboot bootloader""")
	#os.system("""./Tools/platform-tools/fastboot boot ./Tools/TWRP/twrp-2.8.7.1-hammerhead.img""")
	time.sleep(20)
	#os.system('''./Tools/platform-tools/adb pull /data/data/com.whatsapp/databases/msgstore.db dump''')
	hackerPrint("[-] DONE!\n","GOOD", True)

def loadFile(file):
	print("loading file " + file)
	try:
		conn = sqlite3.connect(file)
		c = conn.cursor()
		print("OK")
		for row in c.execute('SELECT * FROM users WHERE uid IN (SELECT uid FROM contacts)'):
			print(row[1])
	except Exception as e:
		raise e

def main():
	args = argsParsing()
	if not args.banner:
		printBanner()
	if args.extract:
		extractApp()
	if args.path:
		loadFile(args.path)

if __name__ == '__main__':
	main()