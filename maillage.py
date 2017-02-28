#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from tkinter import *
import tkMessageBox 
import tkSimpleDialog
import tkFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import os
import numpy as np
import matplotlib.tri as mtri
from fonctions import *
from matplotlib.patches import Polygon
import socket
import threading
import time

#les variables glabales
isConnected = False
#creation de la variable socket associée au client
sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#fonction de connexion au serveur
def Connect():
	global isConnected,sockClient	
	try:
		isConnected = True
		sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sockClient.connect(("127.0.0.1", 1994))
	except:
		tkMessageBox.showerror("connexion", "Démarrer le serveur d'abord pour se connecter'")
		isConnected = False
		
#fonction de déconnexion au serveur		
def disConnect():
	global isConnected,sockClient
	if isConnected==False:
		tkMessageBox.showerror("connexion", "Il faut se connecter d'abord")
	else:
		sockClient.send(str("disconnect").encode())
		isConnected = False

# centrer la fenetre
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

#aide
def aide():
    tkMessageBox.showinfo("aide","C'est une Application client/serveur qui permet de faire:\n"+
							"- un maillage carré\n"+
							"- un maillage triangulaire\n"+
							"- un maillage polygonal\n"+
							"Avant de faire une action, il faut au préalable démarrer le serveur.\n"+
							"Maintenant on entre la taille du maillage qui est envoyé au serveur.\n qui va faire"+
							"le maillage, le stocker dans un fichier et l'envoyer au client. Le client lie le fichier et l'affiche\n"+
							"\n Cette application donne aussi la possibilité à un utilisateur de saisir une fonction affine\n"+
							"ax+by+c grace à laquelle on va colorier les triangles.\n"+
							"On a aussi la possibilité de sauvegarder les fichiers et de les lire.\n"+
							"On enregistre deux fichiers: fichier coordonnées et fichier sommet") 
    
p=1    
#fonction de numérotatoion des triangles du maillage
def num1(i,j):
    return i*(p+1)+j+1

"""Coloriage maillage
prend un tableau de triplets et un tableau des valeurs correspondantes
obtenues en integrant la fonction f(x,y)
"""
def coloriage(tabTriangles, tabIntegrales,traceur,canvas):
	
	tabTriplets = getTabTriplets(tabTriangles)#recuperation du tableau de triplets
	coordsGrav = coordsGravite(tabTriplets)#recuperation coordonnees centres de gravite

	if int(var.get())==3:
		print("Coloriage non disponible")
	else:
		for i in range(0,len(tabTriplets)):
			col = int(round(tabIntegrales[i]*100))
			if col<0:
				col=0
			elif col>=278:
				col=277
			traceur.add_patch(Polygon(tabTriplets[i], closed=True,fill=True, color=COLORS[col]))#on applique la couleur obtenue avec l'integrale
			traceur.add_patch(Polygon(tabTriplets[i], closed=True,fill=False, color='#000000',linestyle='dashdot'))
			traceur.text(coordsGrav[i][0], coordsGrav[i][1], str(i+1), size=2+p%10, ha='center',va='center')
								 
		canvas.show()

#temperature
def temperature():
	if isConnected==False:
		tkMessageBox.showerror("connexion","Veuillez vous connecter au serveur d'abord")
	else:
		q=int(var.get())
		if taille.get()=='' or q==0:
			tkMessageBox.showwarning("info","Veuillez renseigner les champs!")
		elif int(taille.get())==0:
			tkMessageBox.showwarning("info","Donner un entier superieur a 0")
		else:
			fonct_temp=tkSimpleDialog.askstring("f(x,y)=a*x + b*x + c", "Entrer la fonction")
			if(fonct_temp==""):
				tkMessageBox.showerror("Erreur", "Entrer la fonction!")
			else:
				
				ok = True
				try:
					print(fonct_temp)		
					ok = (len(fonct_temp.split('x'))==2) and (len(fonct_temp.split('y'))==2)
				except:
					ok = False		
				if ok:
					
					dlg1 = Toplevel(master=fen)
					dlg1.geometry("900x600")
					
					fig = plt.figure()
					center(dlg1)
					traceur = fig.add_subplot(111)
					canvas = FigureCanvasTkAgg(fig, master=dlg1)
					canvas.get_tk_widget().pack()
					#ajout de la barre de navigation
					toolbar = NavigationToolbar2TkAgg(canvas, dlg1)
					toolbar.update()
					canvas._tkcanvas.pack()
					p=int(taille.get())
					cmd = taille.get()+" "+str(var.get())+" coloriage"
					
					if q==1:
						sockClient.send(cmd.encode())
						for i in range(0,p+1):
								traceur.plot([0,1],[float(i)/p,float(i)/p],'white',lw=2) #tracee des traits horizontaux
								traceur.plot([float(i)/p,float(i)/p],[0,1],'white',lw=2) #tracee des traits verticaux
								traceur.plot([float(i)/p,0],[0,float(i)/p],'white',lw=2) #tracee des traits obliques de la partie basse du carre
								traceur.plot([float(i)/p,1],[1,float(i)/p],'white',lw=2) #tracee des traits obliques de la partie haute du carre
						
					if q==2:
						sockClient.send(cmd.encode())
						for i in range(0,p+1):
								traceur.plot([0,1-float(i)/p],[float(i)/p,float(i)/p],'white',lw=2) #tracee des traits horizontaux
								traceur.plot([float(i)/p,float(i)/p],[0,1-float(i)/p],'white',lw=2) #tracee des traits verticaux
								traceur.plot([float(i)/p,0],[0,float(i)/p],'white',lw=2) # tracee des traits obliques 
					
					coords=sommets=triangles=list
					#recuperation des coordonnees
					coords = getCoords("tmp",int(var.get()),int(p))					
					#recuperation des numeros
					sommets = getSommets("tmp")
					
					triangles = getTriangles(coords,sommets)#recuperation des triangles à colorier
					inteTriangles = getIntegrales(triangles,fonct_temp)#valeurs des integrales au niveau de chaque element fini du maillage
					coloriage(triangles,inteTriangles,traceur,canvas)#application des couleurs		
					
					Button(dlg1, text="Quitter", command=dlg1.destroy,font=("Helvetica", 20),fg='grey').pack(side=LEFT)

					
				else:
					tkMessageBox.showinfo("info!","Entrer une fonction de la forme ax+bx+c")
#sauvegarder du maillage
def sauvegarder():
	if isConnected==False:
		tkMessageBox.showerror("connexion","Veuillez vous connecter au serveur d'abord")
	else:
		nomfic = tkSimpleDialog.askstring("nom du fichier", "Entrer le nom du fichier")
		if nomfic!="" or numfic!=str(None):
			cmd = taille.get()+" "+str(var.get())+" "+nomfic+" sauvegarder"
			q= int(var.get())
			p=int(taille.get())
			enreg= True
			if q==1:
				sockClient.send(cmd.encode())
				sauvegardeRect(nomfic,"carre/",p)
			elif q==2:
				sockClient.send(cmd.encode())
				sauvegardeTri(nomfic,"triangle/",p)
			elif q==3:
				sockClient.send(cmd.encode())
				showinfo("Infos","non defini pour le moment")
			time.sleep(1)
			tkMessageBox.showinfo("Infos","fichier enregistre avec succes")
		else:
			tkMessageBox.showerror("Erreur", "Le nom du fichier ne doit pas etre vide")
	   
#modal maillage    
def button_click():
	if isConnected==False:
		tkMessageBox.showerror("connexion","Veuillez vous connecter au serveur d'abord")
	else:
		q=int(var.get())
		if taille.get()=='' or q==0:
			tkMessageBox.showwarning("info","Veuillez renseigner les champs!")
		elif int(taille.get())==0:
			tkMessageBox.showwarning("info","Donner un entier superieur a 0")
		else:
			time.sleep(1)    
			dlg = Toplevel(master=fen)
			dlg.geometry("900x600")
			fig = plt.figure()
			traceur = fig.add_subplot(111)
			global p
			p=int(taille.get())
			q=int(var.get())
			canvas = FigureCanvasTkAgg(fig, master=dlg)
			canvas.get_tk_widget().pack()
			#ajout de la barre de navigation
			toolbar = NavigationToolbar2TkAgg(canvas, dlg)
			toolbar.update()
			canvas._tkcanvas.pack()
			cmdServeur = taille.get()+" "+str(var.get())+" "+"maillage"
			if q==1:
				sockClient.send(cmdServeur.encode())
				for i in range(0,p+1):
						traceur.plot([0,1],[float(i)/p,float(i)/p],'green',lw=2) #tracee des traits horizontaux
						traceur.plot([float(i)/p,float(i)/p],[0,1],'green',lw=2) #tracee des traits verticaux
						traceur.plot([float(i)/p,0],[0,float(i)/p],'blue',lw=2) #tracee des traits obliques de la partie basse du carre
						traceur.plot([float(i)/p,1],[1,float(i)/p],'blue',lw=2) #tracee des traits obliques de la partie haute du carre
				canvas.show()
			if q==2:
				sockClient.send(cmdServeur.encode())
				for i in range(0,p+1):
						traceur.plot([0,1-float(i)/p],[float(i)/p,float(i)/p],'green',lw=2) #tracee des traits horizontaux
						traceur.plot([float(i)/p,float(i)/p],[0,1-float(i)/p],'green',lw=2) #tracee des traits verticaux
						traceur.plot([float(i)/p,0],[0,float(i)/p],'blue',lw=2) # tracee des traits obliques 
				canvas.show()
			if q==3:
				sockClient.send(cmdServeur.encode())
				x0, y0, r = [0.5]*3
				x=[r*np.cos(2*k*np.pi/p)+x0 for k in range(0,p)]
				y=[r*np.sin(2*k*np.pi/p)+y0 for k in range(0,p)]
				my_tri = mtri.Triangulation(x,y)
				refiner = mtri.UniformTriRefiner(my_tri)
				#plot the original triangulation
				for t in my_tri.triangles:
					t_i = [t[0], t[1], t[2], t[0]]
					traceur.plot(x[t_i],y[t_i] ,'k',linewidth=1.5)
				canvas.show()
			Button(dlg, text="Sauvegarder",font=("Helvetica", 20),fg='grey', command=sauvegarder).pack(side=LEFT)
			Button(dlg, text="Quitter", command=dlg.destroy,font=("Helvetica", 20),fg='grey').pack(side=LEFT)
			dlg.transient(fen)
			dlg.grab_set()
			center(dlg)
#valider champ de saisie
def OnValidate(S):
    if S.isdigit():
        return True
    return False

#ouverture et lecture fichier maillage
def ouvrir_fichier():
	if isConnected==False:
		tkMessageBox.showerror("connexion","Veuillez vous connecter au serveur d'abord")
	else:
		
		cmdServeur = "ouvrirFichier"+" lirefichier" 
		sockClient.send(cmdServeur.encode())
		receivedFiles = tkFileDialog.askopenfilenames(parent=fen, initialdir="/home/mansour/NetBeansProjects/maillage/maillage/fichiers",
							   filetypes =[("Text File", "text {.txt}")],
							   title = "Choisir les fichiers (coordonnées et sommets."
							   )
		filesMaillage = fen.splitlist(receivedFiles)
		print(filesMaillage)
		if len(filesMaillage)==2:
			
			fileCoords = filesMaillage[0]
			fileSoms = filesMaillage[1]
			
			rCoords = fileCoords.split('.')[0]
			rSoms = fileSoms.split('.')[0]
			
			print(rCoords,"\n",rSoms)
			
			rCoords = rCoords[0:len(rCoords)-6]
			rSoms = rSoms[0:len(rSoms)-4]
			
			
			fileOk = rSoms==rCoords
			ext = fileCoords.find("Coords.txt") and fileSoms.find("Soms.txt")
			print(ext)
			if ext==-1 or not fileOk:
				showerror("Erreur fichier", "Les fichiers doivent être de même initial. Exemple *Coords.txt et *Soms.txt")
			else:
				time.sleep(1)
				#tracé du maillage impoté
				dlg1 = Toplevel(master=fen)
				dlg1.geometry("900x600")
				center(dlg1)
				fig = plt.figure()
				traceur = fig.add_subplot(111)
				canvas = FigureCanvasTkAgg(fig, master=dlg1)
				canvas.get_tk_widget().pack()
				#ajout de la barre de navigation
				toolbar = NavigationToolbar2TkAgg(canvas, dlg1)
				toolbar.update()
				canvas._tkcanvas.pack()
				
				#Ouverture de fichiers pour la recuperation des coordonnees
				lignes = list
				with open(fileCoords,"r") as ficCoords:
					lignes = ficCoords.readlines()
				
				#recuperation des coordonnees
				coords = [lignes[i].split(' ') for i in range(0,len(lignes))]
				coords = [[float(coords[i][0]),float(coords[i][1][0:len(coords[i][1])-1])] for i in range(0,len(coords))]
				
				#Ouverture du fichier pour recuperer numeros de sommets
				lignes = list
				with open(fileSoms,"r") as ficSoms:
					lignes = ficSoms.readlines()
				
				#recuperation des numeros
				sommets = [lignes[i].split(' ') for i in range(0,len(lignes))]
				sommets= [[int(float(sommets[i][0])),int(float(sommets[i][1])),int(float(sommets[i][2][0:len(sommets[i][2])-1]))] for i in range(0,len(sommets))]
				
				#recuperation des triangles à colorier
				triangles = getTriangles(coords,sommets)
				
				#recuperation des triplets pour le dessin
				triplets = getTabTriplets(triangles)
				coordsGrav = coordsGravite(triplets)#recuperation coordonnees centres de gravite
				#tracage du maillage
				for i in range(0,len(triplets)):
					traceur.add_patch(Polygon(triplets[i], closed=True,fill=False, color='blue'))#on applique la couleur obtenue avec l'integrale
					traceur.add_patch(Polygon(triplets[i], closed=True,fill=False, color='black'))
				
				canvas.show()
				

		else:
			tkMessageBox.showerror("Chargement fichier", "Deux fichiers de même initial doivent être chargés en même temps")
#quitter	
def quitter():
	if isConnected==True:
		disConnect()
	fen.destroy()
	
fen= Tk()
fen.title('Maillage')
fen['bg']='grey'
fen.geometry("900x600")
fen.minsize(900,600) # taille minimum de la fenetre
fen.maxsize(900,600) # taille maximum de la fenetre
center(fen)
#Creation d'un widget Menu
menubar = Menu(fen, bg='white', activeforeground='grey',font=("Helvetica", 16))
menubar.add_command(label='Fichier',command=ouvrir_fichier)
menuaide = Menu(menubar,tearoff=0,activeforeground='grey',font=("Helvetica", 16))
menuaide.add_command(label="connexion",command=Connect)
menuaide.add_command(label="déconnexion",command=disConnect)
menubar.add_cascade(label="serveur", menu=menuaide)

menubar.add_command(label='Aide', command=aide)
menubar.add_command(label='Quitter', command=quitter)
fen.config (menu = menubar, width = 200, height=300)

#panneau maillage
PanMaillage = Frame(fen, bg='white',width=500,padx=10, pady=10)
PanMaillage.pack(side=RIGHT,fill=Y)
lab=Label(PanMaillage,text='Choisir le type de maillage', bg='white',font=("Helvetica", 20),fg='grey')
lab.grid(row=0)
var = IntVar()
carre=Radiobutton(PanMaillage,text="Carre", variable=var, value=1,bg='white',font=("Helvetica", 16),fg='grey')
carre.grid(row=1)
triangle=Radiobutton(PanMaillage,text="Triangle", variable=var, value=2,bg='white',font=("Helvetica", 16),fg='grey')
triangle.grid(row=2)
polygone=Radiobutton(PanMaillage,text="Polygone", variable=var, value=3,bg='white',font=("Helvetica", 16),fg='grey')
polygone.grid(row=3)
labtaille = Label(PanMaillage, text="Entrer la taille du maillage",bg='white',font=("Helvetica", 20),fg='grey')
labtaille.grid(row=4)
validatecmd = (fen.register(OnValidate), '%S')
taille = Entry(PanMaillage,font=("Helvetica", 20),fg='grey',validate="key",vcmd=validatecmd)
taille.grid(row=5)
valider=Button(PanMaillage, text="Valider",font=("Helvetica", 20),fg='grey', command=button_click)
valider.grid(row=5, column=1)
valider_temp=Button(PanMaillage, text="température",font=("Helvetica", 20),fg='grey', command=temperature)
valider_temp.grid(row=8)
#panneau image
PanImg = Frame(fen, bg='grey',height=600,width=200,padx=10, pady=10)
PanImg.pack(side=LEFT,fill=Y)
can1 = Canvas(PanImg, height =540,width=500, bg ='white')
photo = PhotoImage(file ='maillage.gif')
can1.create_image(200, 260, image =photo)
can1.pack()


fen.mainloop()
