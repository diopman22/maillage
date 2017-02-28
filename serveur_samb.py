#!/usr/bin/python3.4
# coding: utf-8 

import socket
import threading
import time

from fonctions import *#contient de toutes mes fonctions et classes necessaires pour le maillage

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): 
   
        print("Connection de %s %s" % (self.ip, self.port, ))
        while 1:
            r = self.clientsocket.recv(2048).decode()
            print("Reception de la commande ",r,"...")
            data = r.split(' ')
            print(data)
            if len(data)==1 and data[0]=="disconnect":
                self.clientsocket.close()
                break
            elif len(data)==3:
                print("maillage ",data[1],data[2]," avec une taille p =",data[0])
                time.sleep(3)
            elif len(data)==4:
                if data[3]=="coloriage":
                    print("Coloriage ",data[1],data[2]," avec une taille p =",data[0])
                    time.sleep(3)
                if data[3]!="coloriage":
                    print("Stockage ",data[1],data[2]," avec une taille p =",data[0]," avec le nom de fichier ",data[3])
                    print("Fichiers ",data[3]+"Coords.txt ",data[3]+"Soms.txt correspondants créés")
                    time.sleep(3)
        
			

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1993))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
