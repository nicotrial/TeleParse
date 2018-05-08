# -*- coding: utf-8 -*-

from HackerPrint import hackerPrint,hackerPrintErr
import argparse
import sqlite3
import os
import time
import binascii
import struct


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
	parser.add_argument('-f',action='store'		,dest='path'		,required=True, help='Path of db file')
	parser.add_argument('-e',action='store_true',dest='extractApp'		,required=False, help='Autoextract Telegram app from phone')
	parser.add_argument('-ec',action='store_true',dest='extractContacts'		,required=False, help='Show Telegram Messages')
	parser.add_argument('-em',action='store_true',dest='extractMsg'		,required=False, help='Show Telegram Contacts')
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
	except Exception as e:
		raise e
	return c

def extractContacts(c):
		for row in c.execute('SELECT * FROM users WHERE uid IN (SELECT uid FROM contacts)'):
			print(row[1])

def extractMsg(c):
		messagestream = c.execute('SELECT * FROM messages WHERE uid IN (SELECT uid FROM contacts)')
		for row in messagestream:
			tramacursor = 0
			print("---------")
			trama = row[5][tramacursor:tramacursor+4]
			tramacursor = tramacursor + 4
			#print (hex(struct.unpack('<i',trama)[0]))
			header = struct.unpack('<i',trama)[0]
			if header == 0x44f9b43d:
				print("TL_message")
				trama = row[5][tramacursor:tramacursor+4]
				tramacursor = tramacursor + 4
				print (hex(struct.unpack('<i',trama)[0]))
				flags = struct.unpack('<i',trama)[0]
				#print(hex(flags & 2))
				if (flags & 2) is not 0x0:
					print("-out")
				#print(hex(flags & 16))
				if (flags & 16) is not 0x0:
					print("-mentioned")
				#print(hex(flags & 32))
				if (flags & 32) is not 0x0:
					print("-media_unread")
				#print(hex(flags & 8192))
				if (flags & 8192) is not 0x0:
					print("-silent")
				#print(hex(flags & 16384))
				if (flags & 16384) is not 0x0:
					print("-post")
				trama = row[5][tramacursor:tramacursor+4]
				tramacursor = tramacursor + 4
				print (hex(struct.unpack('<i',trama)[0]))
				ids = struct.unpack('<i',trama)[0]
				#print(hex(flags & 16))
				if (flags & 256) is not 0x0:
					print("-from_id")
					trama = row[5][tramacursor:tramacursor+4]
					tramacursor = tramacursor + 4
					from_id = struct.unpack('<i',trama)[0]
					print(from_id)
					#usersstream = c.execute('SELECT name FROM users WHERE uid=164391605')
					#for rowss in usersstream:
					#	print(rowss[0])
				#print(hex(flags & 16))
				if (flags & 4) is not 0x0:
					print("-fwd_from")
				#print(hex(flags & 2048))
				if (flags & 2048) is not 0x0:
					print("-via_bot_id")				
				#print(hex(flags & 8))
				if (flags & 8) is not 0x0:
					print("-reply_to_msg_id")
				#print(hex(flags & 512))
				if (flags & 512) is not 0x0:
					print("-media")
				#print(hex(flags & 64))
				if (flags & 64) is not 0x0:
					print("-reply_markup")
				#print(hex(flags & 128))
				if (flags & 128) is not 0x0:
					print("-magic")
				#print(hex(flags & 1024))
				if (flags & 1024) is not 0x0:
					print("-views")
				#print(hex(flags & 2048))
				if (flags & 32768) is not 0x0:
					print("-edit_date")
				#print(hex(flags & 2048))
				if (flags & 65536) is not 0x0:
					print("-post_author")
				#print(hex(flags & 2048))
				if (flags & 131072) is not 0x0:
					print("-grouped_id")
				

			"""
			trama = row[5][0:4]
			valor = int(binascii.hexlify(trama),16)
			if valor == 0x3db4f944:
				print("Dentro")
				trama = row[5][4:8]
				valor = int(binascii.hexlify(trama),16)
				print(hex(valor))
				print(hex(valor & 0x00000100))
				comp= valor and 0x00000100
				#if comp != 0x0:
				#	print ("Mencionad: ")
				#	print(hex(valor & 0x00008000))
				#	print (row[5])
			"""


def main():
	args = argsParsing()
	if not args.banner:
		printBanner()
	if args.extractApp:
		extractApp()
	if args.path:
		c=loadFile(args.path)
	if args.extractContacts:
		extractContacts(c)
	if args.extractMsg:
		extractMsg(c)

if __name__ == '__main__':
	main()