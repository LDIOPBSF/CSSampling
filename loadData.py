#!C:\Python27
#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import sys
import math
import csv
import re
import random
#from math import log
from LDIOPBSF import *
from tableauItemset import *

delimiteurSequence='-2 '

#tailleMax=int(sys.argv[3])

#Lecture de la base de séquences
def contenuDeMaBase(baseSequence):
	with open(baseSequence, 'r') as base:
		contenu=base.read()
	contenu=contenu.replace('\n',' ') 
	contenu=contenu.replace('\r',' ')
	contenu=contenu[:-2]
	contenu=contenu.split(delimiteurSequence)
	#print "bsf",contenu
	return contenu

#Pondération des des séquences de la base par la cardinalité de leur nombre de sous-séquences distinctes
def maBasePonderee(contenuDeMaBase,tailleMax,indiceClass):
	basePonderee,tabSigma,som,ponderation=[],[],0,{}
	i=1
	for sequence in contenuDeMaBase:
		#print(sequence)
		tabSeq=tableauItemset1(sequence,indiceClass)
		#print(tabSeq)
		#print('i'),i
		M=phi_k(tabSeq,tailleMax)
		#print ('M'),M
		i+=1
		val=0
		if len(M)>0:
			val=sum(M[len(M)-1][1:])
		basePonderee.append(M)
		som+=val
		tabSigma.append(som)
		ponderation[sequence+'-2']=val
		#if i%100==0:
		#	print("Sequence "),i
	return [basePonderee,tabSigma,ponderation]


delimiteurItemset='-1'

#Transformer la séquence en un tableau d'itemsets
def tableauItemset1(sequence,indiceClass):
	k,p=1,0
	if indiceClass>0:
		k=+1 # fin de sequence
	elif indiceClass==0:
		p=1 #debut de sequence
	sequence=sequence.split(delimiteurItemset+' ')
	sequence=sequence[p:-k]
	return sequence

