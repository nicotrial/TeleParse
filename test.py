# -*- coding: utf-8 -*-

from HackerPrint import hackerPrint, hackerPrintErr
import argparse
import sqlite3
import binascii
import struct
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
""" % ('0.1', 'Nicotrial')


def printBanner():
    hackerPrint(banner, "HEAVY", True, 0.01)
    hackerPrint("\n[-] Developed at UAH", "ERROR", True)
    hackerPrintErr("\n[+] AUTHORS : Nicolas Logghe \n", "ERROR", True)


def argsParsing():
    parser = argparse.ArgumentParser(description='Extract data from telegram app')
    parser.add_argument('-f', action='store', dest='path', required=True, help='Path of db file')
    parser.add_argument('-e', action='store_true', dest='extractApp', required=False,
                        help='Autoextract Telegram app from phone')
    parser.add_argument('-ec', action='store_true', dest='extractContacts', required=False,
                        help='Show Telegram Messages')
    parser.add_argument('-em', action='store_true', dest='extractMsg', required=False, help='Show Telegram Contacts')
    parser.add_argument('-b', action='store_true', dest='banner', required=False, help='Do not show Banner')
    args = parser.parse_args()
    return args


def extractApp():
    hackerPrint("[-] Extracting telegram app data from phone\n", "GOOD", True)
    os.system("""./Tools/platform-tools/adb""")
    # os.system("""./Tools/platform-tools/adb reboot bootloader""")
    # os.system("""./Tools/platform-tools/fastboot boot ./Tools/TWRP/twrp-2.8.7.1-hammerhead.img""")
    time.sleep(20)
    # os.system('''./Tools/platform-tools/adb pull /data/data/com.whatsapp/databases/msgstore.db dump''')
    hackerPrint("[-] DONE!\n", "GOOD", True)


def loadFile(file):
    print("loading file " + file)
    try:
        conn = sqlite3.connect(file)
        c = conn.cursor()
        print("OK")
    except Exception as e:
        raise e
    return c, conn


def extractContacts(c, conn):
    for row in c.execute('SELECT * FROM users WHERE uid IN (SELECT uid FROM contacts)'):
        print(row[1])
        print(row[0])
        print("----")

def extractMsg(c, conn):
    # Sacamos dotos los datos de la base de datos de messages
    c.execute('SELECT * FROM messages')
    messagestream = c.fetchall()
    # conn.commit()
    for row in messagestream:
        # solo pillamos el 5 ya que esta es el que contiene el datastream de telegram
        # print (row[5])
        tramacursor = 0
        print("-----====-----")
        #hackerPrint("-----====-----\n", "GOOD", True)
        trama = row[5][tramacursor:tramacursor + 4]
        tramacursor = tramacursor + 4
        #print (hex(struct.unpack('<i',trama)[0]))
        header = struct.unpack('<i', trama)[0]
        print ("Message ID: " + str(row[0]))
        # Aqui vamos viendo la cabeceras de los tadastream
        if header == 0x44f9b43d: #type TL_message
            print (hex(header))
            # Aqui la cabecera es de un mensjae y vamos viendo los flags que tiene activo en cada uno de estas vamos sacando los datos correspondientes si esta activo
            print("TL_message")
            trama = row[5][tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            flags = struct.unpack('<i', trama)[0]
            print ("Flags=" + str(bin(flags)))
            print(hex(flags))
            print(hex(flags & 2))

            if (flags & 2) is not 0x0:
                # Este flag indica que es un mensaje saliente nuestro
                print("---out")

            #print(hex(flags & 16))
            if (flags & 16) is not 0x0:
                print("---mentioned")
                # Este flag indica que hemos sido mencionados en el mensaje

            #print(hex(flags & 32))
            if (flags & 32) is not 0x0:
                print("---media_unread")

            #print(hex(flags & 8192))
            if (flags & 8192) is not 0x0:
                print("---silent")

            #print(hex(flags & 16384))
            if (flags & 16384) is not 0x0:
                print("---post")

            #
            trama = row[5][tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            ids = struct.unpack('<i', trama)[0]
            print ("ID=" + str(ids))

            #print(hex(flags & 16))
            if (flags & 256) is not 0x0:
                print("---from_id")
                trama = row[5][tramacursor:tramacursor + 4]
                tramacursor = tramacursor + 4
                from_id = struct.unpack('<i', trama)[0]
                print(from_id)
                c.execute('SELECT name FROM users WHERE uid=%s' % from_id)
                usersstream = c.fetchall()
                # conn.commit()
                for rowss in usersstream:
                    print(rowss[0])

            #print(hex(flags & 16))
            if (flags & 4) is not 0x0:
                print("---fwd_from")
                trama = row[5][tramacursor:tramacursor + 4]
                tramacursor = tramacursor + 4
                fwd_from = struct.unpack('<i', trama)[0]
                print("    TODO Datos de fwd_from: " + str(fwd_from))
                c.execute('SELECT name FROM users WHERE uid=%s' % fwd_from)
                usersstream = c.fetchall()
                # conn.commit()
                for rowss in usersstream:
                    print(rowss[0])

            #print(hex(flags & 2048))
            if (flags & 2048) is not 0x0:
                print("---via_bot_id")
                trama = row[5][tramacursor:tramacursor + 4]
                tramacursor = tramacursor + 4
                via_bot_id = struct.unpack('<i', trama)[0]
                print("    Datos de via_bot_id=" + str(via_bot_id))

            #print(hex(flags & 8))
            if (flags & 8) is not 0x0:
                print("---reply_to_msg_id: ")
                trama = row[5][tramacursor:tramacursor + 4]
                tramacursor = tramacursor + 4
                reply_to_msg_id = struct.unpack('<i', trama)[0]
                print("    Datos de reply_to_msg_id: " + str(reply_to_msg_id))

            trama = row[5][tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            date = struct.unpack('<I', trama)[0]
            print("DATE=" + str(date))
            epochtime = float(row[4])
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochtime)))

            #print(hex(flags & 512))
            if (flags & 512) is not 0x0:
                # Si es media imprimimos el mesaje hay tambien datos de la ubicacion de el alrchivo guardado hay que intentar sacar esto tambien
                print("---media")
                trama = row[5][tramacursor:]
                tramacursor = tramacursor + 32
                bytes = int(binascii.hexlify(trama[8:9]), 16)
                print (bytes)
                tramacursor = tramacursor + bytes
                message = trama[9:9 + bytes]
                #print(binascii.hexlify(message))
                print(message)
                #print(hex(trama[0:9]))
            else:
                # si no es media lo que hacemos el leer el los primeros bytes que nos dan informacion de el tamaño y con esto mostramos el mensaje (hay mensajes que el tamaño no esta en el mismo lugoar.. si es de mas de 256 caracteres los tamaños de los no se donde estan)
                print("---Regular Message")
                trama = row[5][tramacursor:]
                print(binascii.hexlify(trama))
                print(binascii.hexlify(trama[8:9]))
                tramacursor = tramacursor + 32
                bytes = int(binascii.hexlify(trama[8:9]), 16)
                #bytes = int.from_bytes(trama[0:9], byteorder='little')
                print ("hola")
                print ("Tamañooo")
                print (bytes)
                tramacursor = tramacursor + bytes
                message = trama[9:9 + bytes]
                print(message)

            #print(hex(flags & 64))
            if (flags & 64) is not 0x0:
                print("---reply_markup")

            #print(hex(flags & 128))
            if (flags & 128) is not 0x0:
                print("---magic")

            #print(hex(flags & 1024))
            if (flags & 1024) is not 0x0:
                print("---views")

            #print(hex(flags & 2048))
            if (flags & 32768) is not 0x0:
                print("---edit_date")

            # print(hex(flags & 2048))
            if (flags & 65536) is not 0x0:
                print("---post_author")

            # print(hex(flags & 2048))
            if (flags & 131072) is not 0x0:
                print("---grouped_id")

        else:
            print ("HEADER")
            print (hex(header))

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
        c, conn = loadFile(args.path)
    if args.extractContacts:
        extractContacts(c, conn)
    if args.extractMsg:
        extractMsg(c, conn)


if __name__ == '__main__':
    main()
