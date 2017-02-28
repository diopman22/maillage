#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from tkinter import *
import tkMessageBox 
import tkSimpleDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import os
import numpy as np
import matplotlib.tri as mtri
"""Definition de la classe Point"""
class Point:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	#recuperer les coordonnees sous forme de coule
	def getXY(self):
		return self.x,self.y


"""Definition de la classe triangle"""
class Triangle:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c
	
	#methode qui retourne le triplet
	def getABC(self):
		return self.a.getXY(),self.b.getXY(),self.c.getXY()
		
	#methode qui calcule l'aire d'un triangle
	def aire(self):
		surf = ((self.b.x*self.c.y - self.c.x*self.b.y) + 
		(self.c.x*self.a.y - self.a.x*self.c.y) + (self.a.x*self.b.y - self.b.x*self.a.y))*0.5
		if surf<0:
			return -surf
			
		return surf
		
	
	#calcul de la valeur retournee par une fonction en un sommet donne
	#un sommet est identifie par un numero (1 2 3)
	#f est une chaine de caractere à évaluer
	def calculFonct(self, f, som):
		x=y=0	#les variables à inclure dans l'évaluation
		ff = f
		if som==1:
			x = self.a.x
			y = self.a.y
		if som==2:
			x = self.b.x
			y = self.b.y
		if som==3:
			x = self.c.x
			y = self.c.y
		return eval(ff)
		
		
	#methode qui calcule l'integrale d'un triangle vis à vis de la fonction f
	#f sera représentée sous forme d'un tableau de monômes
	def integrale(self, f):
		inte = 1
		inte = inte*self.aire()/3
		fabc = self.calculFonct(f,1)+self.calculFonct(f,2)+self.calculFonct(f,3)
		inte *= fabc
		return inte


#p=1#variable globale initialisée à 1, a definir au niveau du serveur

#tableau des couleurs
COLORS = []
with open('fichiers/config/colors.txt','r') as ficColor:
	COLORS=ficColor.readlines()

COLORS = [COLORS[i][0:len(COLORS[i])-1] for i in range(0,len(COLORS))]

#fonction qui enleve les doublons dans une liste
def skip_duplicates(iterable, key=lambda x: x):
 
    # on va mettre l’empreinte unique de chaque élément dans ce set
    fingerprints = set()
 
    for x in iterable:
        # chaque élement voit son emprunte calculée. Par défaut l’empreinte
        # est l'élément lui même, ce qui fait qu'il n'y a pas besoin de
        # spécifier 'key' pour des primitives comme les ints ou les strings.
        fingerprint = key(x)
 
        # On vérifie que l'empreinte est dans la liste des empreintes  des
        # éléments précédents. Si ce n'est pas le cas, on yield l'élément, et on
        # rajoute sont empreinte dans la liste de ceux trouvés, donc il ne sera
        # pas yieldé si on ne le yieldera pas une seconde fois si on le
        # rencontre à nouveau
        if fingerprint not in fingerprints:
            yield x
            fingerprints.add(fingerprint)
            
            
#fonction de numerotatoion des triangles du maillage
def num1(i,j,p):
	return i*(p+1)+j+1

#fonction de numerotation des triangles d'un domaine triangulaire
def num2(i,j,p):
	return j*(p+1)-round(j*(j-1)/2) +i+1
	
	            
#fonction qui retourne les coordonnees des points du maillage polygonal
def unit_poly_verts(p):
	x0, y0 = [0.5] * 2
	x=[]
	y=[]
	for i in range(1,2*p):
		r = 0.5/i
		for j in range(0,p):
			x.append(r*np.cos(2*j*np.pi/p)+x0)
			y.append(r*np.sin(2*j*np.pi/p)+y0)
	
	#suppression des doublons		
	x = list(skip_duplicates(x))
	y = list(skip_duplicates(y))
	
	print(x)
	print(y)
	
	if (len(x)>len(y)):
		return x[0:len(y)],y
	else:
		return x,y[0:len(x)]
	

"""sauvegarde maillage rectangulaire"""
def sauvegardeRect(nomfic,rep,p):
	fichierCoords = open("fichiers/"+rep+"/"+nomfic+"Coords.txt", "w")
	for j in range(0,p+1):
		for i in range(0,p+1):
			coords = str(float(i)/p)+" "+str(float(j)/p)+"\n"
			fichierCoords.write(coords)

	fichierCoords.close()

	#enregistrement des numeros de sommets de premiere categorie
	fichierSom = open("fichiers/"+rep+"/"+nomfic+"Soms.txt", "w",p)
	for i in range(0,p):
		for j in range(0,p):
			soms = str(num1(i,j,p))+" "+str(num1(i+1,j,p))+" "+str(num1(i,j+1,p))+"\n"
			fichierSom.write(soms)

	#enregistrement des sommets de seconde categorie
	for i in range(1,p+1):
		for j in range(1,p+1):
			soms = str(num1(i,j,p))+" "+str(num1(i-1,j,p))+" "+str(num1(i,j-1,p))+"\n"
			fichierSom.write(soms)

	fichierSom.close()
	
"""sauvegarde maillage triangulaire"""
def sauvegardeTri(nomfic,rep,p):
	fichierCoords = open("fichiers/"+rep+""+nomfic+"Coords.txt", "w")
	for j in range(0,p+1):
		for i in range(0,p+1-j):
			coords = str(float(i)/p)+" "+str(float(j)/p)+"\n"
			fichierCoords.write(coords)

	fichierCoords.close()
	
	#enregistrement des numeros de sommets de premiere categorie
	fichierSom = open("fichiers/"+rep+""+nomfic+"Soms.txt", "w")
	for j in range(0,p):
		for i in range(0,p-j):
			soms = str(num2(i,j,p))+" "+str(num2(i,j+1,p))+" "+str(num2(i+1,j,p))+"\n"
			fichierSom.write(soms)
			
	#enregistrement des triangles de seconde categorie
	for j in range(1,p):
		for i in range(0,p-j):
			soms = str(num2(i+1,j,p))+" "+str(num2(i+1,j-1,p))+" "+str(num2(i,j,p))+"\n"
			fichierSom.write(soms)

	fichierSom.close()


"""Fonction de recuperation des coordonnees
Elle prend en entree un fichier et un repertoire
"""
def getCoords(nomfic,typemaillage,p):
	lignes=list
	
	#sauvegarde du maillage
	if typemaillage==1:
		sauvegardeRect(nomfic,"",p)
	elif typemaillage==2:
		sauvegardeTri(nomfic,"",p)
		
	#ouverture fichier des coordonnees
	with open("fichiers/"+nomfic+"Coords.txt","r") as ficCoords:
		lignes = ficCoords.readlines()
	
	#recuperation des coordonnees
	coords = [lignes[i].split(' ') for i in range(0,len(lignes))]
	coords = [[float(coords[i][0]),float(coords[i][1][0:len(coords[i][1])-1])] for i in range(0,len(coords))]
	
	return coords


"""Fonction de recuperation des sommets
Elle prend en entree un fichier et un repertoire
"""
def getSommets(nomfic):
	#ouverture fichier des numeros de triangle
	lignes=list
	with open("fichiers/"+nomfic+"Soms.txt","r") as ficSoms:
		lignes = ficSoms.readlines()
	
	#recuperation des numeros
	sommets = [lignes[i].split(' ') for i in range(0,len(lignes))]
	sommets= [[int(float(sommets[i][0])),int(float(sommets[i][1])),int(float(sommets[i][2][0:len(sommets[i][2])-1]))] for i in range(0,len(sommets))]
	
	return sommets

"""Fonction de recuperation des coordonnees des centres de gravite de chaque
triangle du maillage afin de faire la numerotation
argument: tableau de triplets de point(x,y)
"""	
def coordsGravite(tabTriplets):
	return [[(tabTriplets[i][0][0]+tabTriplets[i][1][0]+tabTriplets[i][2][0])/3,
	(tabTriplets[i][0][1]+tabTriplets[i][1][1]+tabTriplets[i][2][1])/3] for i in range(0,len(tabTriplets))]
	


"""Fonction qui retourne un tableau de triangle 
a partir d'un  tableau de coordonnees et d'un tableau de triplets(de numeros de 3 sommets)
"""
def getTriangles(tabCoords, tabSoms):
	return [Triangle(Point(tabCoords[tabSoms[i][0]-1][0],tabCoords[tabSoms[i][0]-1][1]),
	Point(tabCoords[tabSoms[i][2]-1][0],tabCoords[tabSoms[i][2]-1][1]),
	Point(tabCoords[tabSoms[i][1]-1][0],tabCoords[tabSoms[i][1]-1][1])) for i in range(0,len(tabSoms))]	


"""Fonction qui retourne un tableau des integrales des triangles
afin de faire le coloriage pour la fonction de temperature
"""
def getIntegrales(tabTriangles, f):
	return [tabTriangles[i].integrale(f) for i in range(0,len(tabTriangles))]
	
"""Fonction qui retourne un tableau de triplets a partir d'un tableau de triangles"""
def getTabTriplets(tabTri):
	return [tabTri[i].getABC() for i in range(0,len(tabTri))]
