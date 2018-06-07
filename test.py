# -*- coding: utf-8 -*-

import argparse
import sqlite3
import binascii
import struct
import os
import re
import sys
from HackerPrint import hackerPrint, hackerPrintErr
import time

reload(sys)
sys.setdefaultencoding('utf8')

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
    parser.add_argument('-e', action='store_true', dest='extractApp', required=False,help='Autoextract Telegram app from phone')
    parser.add_argument('-ec', action='store_true', dest='extractContacts', required=False,help='Show Telegram Messages')
    parser.add_argument('-eu', action='store_true', dest='extractUsers', required=False,help='Show Telegram Users')
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
    print("----------=======Extracting Known Contacts=======-------------")
    for row in c.execute('SELECT * FROM users WHERE uid IN (SELECT uid FROM contacts)'):
        print(row[1])
        print(row[0])
        print("----------==============-------------")

def extractUsers(c, conn):
    print("----------=======Extracting last Messages=======-------------")
    c.execute('SELECT * FROM dialogs WHERE did IN (SELECT uid FROM users)')
    resultado = c.fetchall()
    for row in resultado:
        c.execute('SELECT * FROM users WHERE uid IS ' + str(row[0]))
        resultado1 = c.fetchall()
        for row1 in resultado1:
            print(row1[1])
        c.execute('SELECT * FROM messages WHERE mid IS ' + str(row[3]))
        resultado2 = c.fetchall()
        for row2 in resultado2:
            epochtime = row2[4]
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochtime)))
            data = decodeMsg(c, conn,row2[5])
            print(data)
            print("HeaderHEX: "+str(data[0]))
            print("HeaderType: " + str(data[1]))
            print("Flags: " + str(data[2]))
            print("Ids: " + str(data[3]))
            print("TramaMensaje: " + str(data[4]))
            print("MessageSize: " + str(data[5]))
            print("Message: " + str(data[6]))
            print("Date: " + str(data[7]))
            print("TimeStamp: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[8]))))
            print("Fromuid: " + str(data[9]))
            print("fwd_from_name: " + str(data[10]))
            print("fwd_id_name: " + str(data[11]))
            print("UsernameUsers: " + str(data[12]))
            print("UsernameChats: " + str(data[13]))

        print("----------==============-------------")

def extractBots(c, conn):
    print("----------=======Extracting Bots info=======-------------")
    for row in c.execute('SELECT * FROM bot_info'):
        for match in re.finditer(('([\w/]{%s}[\w/]*)' % 1).encode(),row[1]):
            print (match.group(0)),
        print("\n")
        print(row[0])
        print("----------==============-------------")

def extractBlockedUsers(c, conn):
    print("----------=======Extracting Blocked Users=======-------------")
    for row in c.execute('SELECT * FROM contacts WHERE uid IN (SELECT uid FROM blocked_users)'):
        print(row)
        print("----------==============-------------")

def extractUsers1(c, conn):
    print("----------=======Extracting All Users=======-------------")
    for row in c.execute('SELECT * FROM users'):
        print(row[1])
        print(row[0])
        print("----------==============-------------")


def decodeMsg(c, conn, message):
    usernameUsers = ""
    usernameChats = ""
    flagsActive = []
    fromuid = 0
    tramaMsg = ""
    timestamp = 0.0
    size = 0
    fwd_from_name = ""
    fwd_id_name = ""



    # solo pillamos el 5 ya que esta es el que contiene el datastream de telegram
    # print (row[5])
    tramacursor = 0
    trama = message[tramacursor:tramacursor + 4]
    tramacursor = tramacursor + 4
    header = struct.unpack('<i', trama)[0]
    # Aqui vamos viendo la cabeceras de los tadastream
    if header == 0x44f9b43d:  # type TL_message
        # Aqui la cabecera es de un mensjae y vamos viendo los flags que tiene activo en cada uno de estas vamos sacando los datos correspondientes si esta activo
        messagetype = "TL_message"
        trama = message[tramacursor:tramacursor + 4]
        tramacursor = tramacursor + 4
        flags = struct.unpack('<i', trama)[0]

        if (flags & 2) is not 0x0:
            # Este flag indica que es un mensaje saliente nuestro
            flagsActive.append("out")

        # print(hex(flags & 16))
        if (flags & 16) is not 0x0:
            # Este flag indica que hemos sido mencionados en el mensaje
            flagsActive.append("mentioned")

        # print(hex(flags & 32))
        if (flags & 32) is not 0x0:
            flagsActive.append("media Unread")

        # print(hex(flags & 8192))
        if (flags & 8192) is not 0x0:
            flagsActive.append("silent")

        # print(hex(flags & 16384))
        if (flags & 16384) is not 0x0:
            flagsActive.append("post")

        #
        trama = message[tramacursor:tramacursor + 4]
        tramacursor = tramacursor + 4
        ids = struct.unpack('<i', trama)[0]

        # print(hex(flags & 16))
        if (flags & 256) is not 0x0:
            flagsActive.append("fromu_id")
            trama = message[tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            from_id = struct.unpack('<i', trama)[0]
            c.execute('SELECT name FROM users WHERE uid=%s' % from_id)
            usersstream = c.fetchall()
            # conn.commit()
            for rowss in usersstream:
                fwd_id_name = rowss[0]

        # print(hex(flags & 16))
        if (flags & 4) is not 0x0:
            flagsActive.append("fwd_from")
            trama = message[tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            fwd_from = struct.unpack('<i', trama)[0]
            c.execute('SELECT name FROM users WHERE uid=%s' % fwd_from)
            usersstream = c.fetchall()
            # conn.commit()
            for rowss in usersstream:
                fwd_from_name=rowss[0]

        # print(hex(flags & 2048))
        if (flags & 2048) is not 0x0:
            flagsActive.append("via_bot_id")
            trama = message[tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            via_bot_id = struct.unpack('<i', trama)[0]
            #print("    Datos de via_bot_id=" + str(via_bot_id))

        # print(hex(flags & 8))
        if (flags & 8) is not 0x0:
            flagsActive.append("replay_to_msg_id")
            trama = message[tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            reply_to_msg_id = struct.unpack('<i', trama)[0]
            #print("    Datos de reply_to_msg_id: " + str(reply_to_msg_id))

        trama = message[tramacursor:tramacursor + 4]
        tramacursor = tramacursor + 4
        date = struct.unpack('<I', trama)[0]

        # print(hex(flags & 512))
        if (flags & 512) is not 0x0:
            # Si es media imprimimos el mesaje hay tambien datos de la ubicacion de el alrchivo guardado hay que intentar sacar esto tambien
            flagsActive.append("media")
            trama = message[tramacursor:]
            tramaMsg = binascii.hexlify(trama)
            fromuid = struct.unpack('<i', trama[0:4])[0]
            c.execute('SELECT name FROM chats WHERE uid=%s' % fromuid)
            chatsstream = c.fetchall()
            for rowss in chatsstream:
                usernameChats = rowss[0]
            c.execute('SELECT name FROM users WHERE uid=%s' % fromuid)
            chatsstream = c.fetchall()
            for rowss in chatsstream:
                usernameUsers = rowss[0]
            bytes = int(binascii.hexlify(trama[8:9]), 16)
            timestamp = struct.unpack('<i', trama[4:8])[0]
            tramacursor = tramacursor + bytes
            message = str(trama[9:9 + bytes])

            f = open('workfile', 'a')
            f.write(str(message))
            f.close()
        else:
            # si no es media lo que hacemos el leer el los primeros bytes que nos dan informacion de el tamaño y con esto mostramos el mensaje (hay mensajes que el tamaño no esta en el mismo lugoar.. si es de mas de 256 caracteres los tamaños de los no se donde estan)
            flagsActive.append("regularMessage")
            trama = message[tramacursor:]
            tramaMsg = binascii.hexlify(trama)
            fromuid = struct.unpack('<i', trama[0:4])[0]
            c.execute('SELECT name FROM chats WHERE uid=%s' % fromuid)
            chatsstream = c.fetchall()
            for rowss in chatsstream:
                usernameChats = rowss[0]
            c.execute('SELECT name FROM users WHERE uid=%s' % fromuid)
            chatsstream = c.fetchall()
            # conn.commit()
            for rowss in chatsstream:
                usernameUsers = rowss[0]
            timestamp = struct.unpack('<i', trama[4:8])[0]
            tramacursor = tramacursor + 32
            bytes = int(binascii.hexlify(trama[8:9]), 16)
            # bytes = int.from_bytes(trama[0:9], byteorder='little')
            size = bytes
            tramacursor = tramacursor + bytes
            message = str(trama[9:9 + bytes])

        # print(hex(flags & 64))
        if (flags & 64) is not 0x0:
            print("---reply_markup")
            flagsActive.append("reply_markup")
            trama = message[tramacursor:tramacursor + 4]
            tramacursor = tramacursor + 4
            #reply_markup = struct.unpack('<i', trama)[0]
            #print("    Datos de reply_markup: " + str(reply_markup))

        # print(hex(flags & 128))
        if (flags & 128) is not 0x0:
            flagsActive.append("magic")
            tramacursor = tramacursor + 4

        # print(hex(flags & 1024))
        if (flags & 1024) is not 0x0:
            flagsActive.append("views")
            tramacursor = tramacursor + 4

        # print(hex(flags & 2048))
        if (flags & 32768) is not 0x0:
            flagsActive.append("edit_date")
            tramacursor = tramacursor + 4

        # print(hex(flags & 2048))
        if (flags & 65536) is not 0x0:
            flagsActive.append("post_author")

        # print(hex(flags & 2048))
        if (flags & 131072) is not 0x0:
            flagsActive.append("grouped_id")

        texto = (message.replace("\00", "")).decode('utf-8', 'ignore')
        return([hex(header),messagetype,str(flagsActive),str(ids),str(tramaMsg),size,str(texto).strip(),date,timestamp,fromuid,fwd_from_name,fwd_id_name,usernameUsers,usernameChats])
    else:
        messagetype = "Other"
        return([hex(header), messagetype, "", "", "", 0, "", 0.0,0.0,"","","","",""])



def extractMsg(c, conn):
    from elasticsearch import Elasticsearch

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    import requests
    res = requests.get('http://localhost:9200')
    # print(res.content)

    settings1 = {
        "mappings": {
            "telegram": {
                "properties": {
                    "date": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                }
            },
        }
    }
    res1 = es.indices.create(index='testing', ignore=400, body=settings1)

    # Sacamos dotos los datos de la base de datos de messages
    c.execute('SELECT * FROM messages')
    messagestream = c.fetchall()
    # conn.commit()
    for row in messagestream:
        data = decodeMsg(c, conn, row[5])
        #print(data)
        #print("HeaderHEX: " + str(data[0]))
        #print("HeaderType: " + str(data[1]))
        #print("Flags: " + str(data[2]))
        #print("Ids: " + str(data[3]))
        #print("TramaMensaje: " + str(data[4]))
        #print("MessageSize: " + str(data[5]))
        #print("Message: " + str(data[6]))
        #print("Date: " + str(data[7]))
        #print("TimeStamp: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[8]))))
        #print("Fromuid: " + str(data[9]))
        #print("fwd_from_name: " + str(data[10]))
        #print("fwd_id_name: " + str(data[11]))
        #print("UsernameUsers: " + str(data[12]))
        #print("UsernameChats: " + str(data[13]))

        res1 = es.index(
            index="testing",
            doc_type="telegram",
            id=int(float(data[8]) * 1000.0),
            body={
                "msg.Header": data[0],
                "msg.HeaderType": str(data[1]),
                "msg.Flags": str(data[2]),
                "msg.Id": str(data[3]),
                "msg.MsgTrama": str(data[4]),
                "msg.MsgSize": str(data[5]),
                "msg.MsgText": str(data[6]),
                "msg.Date": str(data[7]),
                "msg.FromUid": str(data[9]),
                "msg.FwdFromName": str(data[10]),
                "msg.FwdIdName": str(data[11]),
                "msg.UsernameUsers": str(data[12]),
                "msg.UsernameChats": str(data[13]),
                "date": int(float(data[8]) * 1000.0)
            }
        )
        print(res1)
        print("done")


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
    if args.extractUsers:
        extractUsers(c, conn)


if __name__ == '__main__':
    main()
