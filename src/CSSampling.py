
#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import sys
import math
import csv
import re
import random
import functools
from sousSequence import *
import time

#It requires 4 arguments before running
if len(sys.argv) < 4:
	print( "Erreur d'entrée!")
	sys.exit()

############################## Some functions ############################

#Sort two tables tab1 and tab2 as tab1[i]~tab2[i] for all i
def triSelection(tab1,tab2):
	tab=[]
	tailleTab = len(tab1)
	for i in range(tailleTab) : 
		k= i
		for j in range(i+1,tailleTab) :
			if tab1[k] > tab1[j] :
				k = j
		tab1[k],tab1[i] = tab1[i],tab1[k]
		tab2[k],tab2[i] = tab2[i],tab2[k]
	tab.append(tab1),tab.append(tab2)
	return tab



def compare(x,y):
	if x<y: return -1
	if x==y: return 0
	if x>y: return 1

def compareElem2(tuple1,tuple2):
	return compare(tuple1[0],tuple2[0])

def trier(matrice):
	return sorted(matrice, key = functools.cmp_to_key(compareElem2))

#################################### the main program ##########################

baseSequence=sys.argv[1] #the complete path of the dataset
k,N=0,int(sys.argv[2]) # N is the size of the sample
tailleMax=int(sys.argv[3]) # the maximun norm constrain
indiceClass=int(sys.argv[4]) # the index of the attribute to predict
tailleMin = 1

tmps21=time.clock()
contenuBaseSequence=contenuDeMaBase(baseSequence) #loading the dataset
result =maBasePonderee(contenuBaseSequence,tailleMax,indiceClass) #ponderation of the sequences database


tmps22=time.clock()-tmps21
print ("Duree pretraitement = "), tmps22
	
basePonderee,tabSigma=result[0],result[1]

tmps21=time.clock()
EnsSousSequence, EnsSequence=[],{}
nombreDeRejet,c_accept, c_rejet=0,0,0

tableauPhiSequence,tableauNbApparitionSequence=[],[]
i=0

# Sampling N patterns
while i<N:
	mesValParam=BSF(EnsSequence, EnsSousSequence,nombreDeRejet,contenuBaseSequence,basePonderee,c_accept, c_rejet,tabSigma, tailleMax,tailleMin, indiceClass)
	nombreDeRejet,c_accept, c_rejet=mesValParam[0],mesValParam[1],mesValParam[2]
	i+=1

tmps22=time.clock()-tmps21
print ("Duree tirage = "), tmps22
tmps2=time.clock()-tmps1

#output. We take the Samples as output folder by default
relation=baseSequence.split("\\")[1].split(".")[0]
ficSample=""
for i in range(len(EnsSousSequence)):
	ficSample=ficSample+EnsSousSequence[i]+"-2\n"

print ("Taux d'acceptation reel : "),float(N)/(N+nombreDeRejet)
with open('Samples/'+str(tailleMax)+'_'+relation+'_'+str(N)+'.txt', 'w') as fic:
	fic.write(ficSample)
print ("################## Duree totale d'execution D = "), tmps2
			
print ("************************************************* ")

