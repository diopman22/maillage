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
            elif len(data)==2:
				print("lecture fichier....")

            elif len(data)==3:
				if data[2]=="maillage":
					if data[1]=="1":
						print("maillage domaine carre avec une taille p =",data[0])
						print("traitement du maillage carre...")
						time.sleep(0.5)
						print("envoi du fichier maillage...")
						time.sleep(0.5)
						print("reussi")
					elif data[1]=="2":
						print("maillage domaine triangle avec une taille p =",data[0])
						print("traitement du maillage triangulaire...")
						time.sleep(0.5)
						print("envoi du fichier maillage...")
						time.sleep(0.5)
						print("reussi")
					elif data[1]=="1":
						print("maillage domaine polygone avec une taille p =",data[0])
						print("traitement du maillage...")
						time.sleep(0.5)
						print("envoi du fichier maillage...")
						time.sleep(0.5)
						print("reussi")
				elif data[2]=="coloriage":
					if data[1]=="1":
						print("coloriage domaine carre avec une taille p =",data[0])
						print("traitement du coloriage ...")
						time.sleep(0.5)
						print("envoi ...")
						time.sleep(0.5)
						print("reussi")
					elif data[1]=="2":
						print("coloriage domaine triangle avec une taille p =",data[0])
						print("traitement du maillage...")
						time.sleep(0.5)
						print("envoi du fichier maillage...")
						time.sleep(0.5)
						print("reussi")
					elif data[1]=="1":
						print("coloriage domaine polygone avec une taille p =",data[0])
            elif len(data)==4:
				if data[1]=="1":
					print("Stockage carre avec une taille p =",data[0]," avec le nom de fichier ",data[2])
					print("traitement de la sauvegarde...")
					time.sleep(3)
					print("reussi")
				elif data[1]=="2":
					print("Stockage triangle avec une taille p =",data[0]," avec le nom de fichier ",data[2])
					print("traitement de la sauvegarde...")
					time.sleep(3)
					print("reussi")
				print("Fichiers ",data[2],"Coords.txt ",data[2],"Soms.txt correspondants créés")
			
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("127.0.0.1",1994))

while True:
    tcpsock.listen(10)
    print( "Serveur en écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
