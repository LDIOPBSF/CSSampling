#!C:\Python27
#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import sys
import math
import csv
import re
import random
from tirageAleatoireSequence import *
from tableauItemset import *
from loadData import *
from mpmath import mpf


#Récupération du nom de la base passé en argument
#baseSequence=sys.argv[1]


#contenuBaseSequence=contenuDeMaBase(baseSequence)
#basePonderee=maBasePonderee(contenuBaseSequence)
#print "Nombre de sequences dans la base ",len(basePonderee)
	
#pile ou face
def pile():
	return (random.randint(0,1)==1)

#itemset1 privé de l'itemset2
def prive(itemset1,itemset2,indiceClass):
	p,k=0,1
	if indiceClass>0:
		k+=1
	else:
		p=1
	itemset1=itemset1.split(' ')[:-1]
	itemset2=itemset2.split(' ')[p:-k]
	#print ('itemset1,itemset2'),itemset1,itemset2
	itemset=[]
	for item in itemset1:
		if item not in itemset2:
			itemset.append(item)
	return ' '.join(itemset)+' '


def k_norme(tabNorme):
	tab=[]
	som=0
	for val in tabNorme:
		som+=val
		tab.append(som)
	i,j=0,len(tab)-1
	alea=random.random()*tab[j]
	#print (alea)
	k=trouver(tab,i,j+1,alea)
	#print "tabNorme",tabNorme,alea,k,tab
	return k+1
	


#Tirage aléatoire d'une sous-séquence
def sousSequence(sequence2, nombreDeRejet,tabNorme,indiceClass):
	#print "sequence2",sequence2
	#print "**********************"
	#normeSeq=normeTabItemset(sequence2)
	sousSequence=[]
	tailleItemRej,tRejet=0,0
	rejet=True
	#nombreDeRejet=0
	maSeq,Tab=[],[]
	maSeq='-1 '.join(sequence2).split(' ')[:-1]
	if indiceClass==len(sequence2)-1:
		indiceClass=len(maSeq)-1
	Tab[:]=[i for i in range(len(maSeq)) if str(maSeq[i])!='-1' and i!=indiceClass]
	#print ('Tab',Tab)
	x=k_norme(tabNorme)#identite(min(tailleMax,normeSeq))
	#print 'x,normeSeq',x,normeSeq
	T,L=[],[]
	while rejet==True:
		T[:]=list(Tab)
		X=[]
		for i in xrange(x):			
			m=random.randint(0,len(T)-1)
			X.append(T[m])
			T.remove(T[m])
			#print 'T,X',T,X
		L=[]
		f=0
		while f< len(maSeq):
			if f in X or maSeq[f]=='-1':
				L.append(maSeq[f]+' ')
			else:
				L.append('')
			
			f+=1
		L=''.join(L).split('-1 ')
		#print ('L'),L
		#print ('S'),sequence2
		n=len(L)-1
		rejet=False
		while n>0 and rejet==False:
			if len(L[n]) != 0:
				#print 'L[n]',"'"+L[n]+"'"
				k=n-1
				while k>=0 and rejet==False and L[k] in ' ':
					if prive(L[n],sequence2[k],indiceClass) not in ' ':
						#sys.exit()
						k-=1
					else:
						#print 'L',L,'\n Seq',sequence2,'k',k
						#print 'n,k',n,k
						L=[]
						rejet=True
						nombreDeRejet+=1
						#print "Rejet",nombreDeRejet
						#sys.exit()
						tailleItemRej+=x
			n-=1
		#print ('rejet'),rejet
	accep=x
	sousSequence=[b for b in L if b !='']
	#print ('sousSequence'),sousSequence,('\n Norme '),accep,('\n NormetabItemset'),normeTabItemset(sousSequence),('\n nombreDeRejet'),nombreDeRejet
	#print ("**********************")
	return [sousSequence,nombreDeRejet,accep,tailleItemRej]




def nbItemset(seq):
	nbitemset=0
	if seq!=[]:
		for f in seq:
			if f not in '  ':
				nbitemset+=1
	return nbitemset

def ensembleItems(sequence2):
	ens,t=set(),[]
	for i in range(0,len(sequence2)):
		a=sequence2[i].split(' ')[:-1]
		if len(a)>0:
			ens=ens.union(a)
	t[:] = [i for i in ens if len(i)!=0]
	return t
		


def priveXdansT(X,T):
	return [e for e in T if e not in X]


#Génération d'une sous-séquence de la séquance tirée aléatoirement dans la base de séquence
def BSF(EnsSequence, EnsSousSequence,nombreDeRejet,contenuBaseSequence,basePonderee, c_accept, c_rejet,tabSigma,tailleMax,indiceClass):
	SousSeq_Ind=tirageSequence(contenuBaseSequence,basePonderee,tabSigma)
	maSequence=tableauItemset(SousSeq_Ind[0])
	M=SousSeq_Ind[1] #phi_k(maSequence,tailleMax)
	#print "M",M
	#print "SousSeq_Ind[1]",SousSeq_Ind[1]
	#print(maSequence),len(maSequence)
	#print(M[len(M)-1][1:])
	result=sousSequence(maSequence,nombreDeRejet,M[len(M)-1][1:],indiceClass)
	maSousSequence=result[0]
	nombreDeRejet=result[1]
	c_accept+=result[2]
	c_rejet+=result[3]
	sousSeq=""
	for itemset in maSousSequence:
		if itemset!=' ':
			sousSeq+=itemset+delimiteurItemset+" "


	#if sousSeq in EnsSousSequence.keys():
	#	EnsSousSequence[sousSeq]+=1
	#else:
	#	EnsSousSequence[sousSeq]=1
	EnsSousSequence.append(sousSeq)

	delimiteurI=delimiteurItemset+' '
	maSequence= delimiteurI.join(maSequence)+delimiteurItemset+' '+delimiteurSequence
	if maSequence in EnsSequence.keys():
		EnsSequence[maSequence]+=1
	else:
		EnsSequence[maSequence]=1
	return [nombreDeRejet,c_accept, c_rejet]


#Inclusion entre itemsets de séquences sachant que les items sont ordonnés
def inclus(itemset1, itemset2):
	itemset1=itemset1.split(' ')
	itemset2=itemset2.split(' ')
	for f in itemset1:
		if f not in itemset2:
			return False
	return True
	

#Est-ce une sous-séquence d'une séquence
def EstSousSequence(sousSeq, sequence, indiceClass):
	tab1=sousSeq.split(' -1 ')[:-1]
	tab2=sequence.split(' -1 ')[:-1]
	#print(tab1),(tab2)
	if len(tab1)>len(tab2):
		return False
	i,j,ok, taille1,taille2=0,0,True,len(tab1),len(tab2)
	while i<taille1 and ok:
		while j<taille2 and not inclus(tab1[i], tab2[j]): 
			j+=1
		if j==taille2:
			ok=False	
		else:
			j+=1
		i+=1
	return ok==True
	

#Support cardinal
def supportCardinal(contenuBaseSequence,sousSequence,indiceClass):
	#if len(sousSequence)<3: print sousSequence
	som=0
	for sequence in contenuBaseSequence:
		if EstSousSequence(sousSequence,sequence,indiceClass)==True:
			som+=1
			#print sequence+delimiteurSequence
	#print som
	return som

#Fréquence
def frequence(contenuBaseSequence,sousSequence,indiceClass):
	return float(supportCardinal(contenuBaseSequence,sousSequence,indiceClass))/len(contenuBaseSequence)


#Norme d'une séquence à partir de sa forme brute, ex : 12 2 -1 3 5 -1 
def norme(sequence):
	sequence=sequence.replace('-1 ', '').split(' ')[:-1]
	som=0
	for f in sequence:
		if f not in '  ':
			som+=1
	return som

#Norme d'une séquence à partir de son tableau d'itemsets correspondant 
def normeTabItemset(tabItemset):
	sequence='-1 '.join(tabItemset).replace('-1 ', '').split(' ')[:-1]
	som=0
	for f in sequence:
		if f not in '  ':
			som+=1
	return som


def sommeComb(contenuBaseSequence,i,k1,k2):
	val,n=0,norme(contenuBaseSequence[i])
	for i in range(k1,k2+1):
		val+=combin(n,i)
	return val


#Nombre moyen de tirages
def nombreMoyenDeTirages(contenuBaseSequence,basePonderee,tabSigma,k1,k2):
	tmps1=time.clock()
	LongueurBase,i =len(contenuBaseSequence),0
	somme=tabSigma[LongueurBase-1]
	tauxAcceptation=0
	while i<LongueurBase:
		#print(i),(basePonderee[i])
		#print(contenuBaseSequence[i])
		mu=mpf(sommeComb(contenuBaseSequence,i,k1,k2))/mpf(sum(basePonderee[i][len(basePonderee[i])-1][1:]))
		tauxAcceptation+=mpf(mpf(sum(basePonderee[i][len(basePonderee[i])-1][1:]))/mpf(somme))*mu
		i+=1
	dureeTotale=time.clock()-tmps1
	#print "dureeTotale",dureeTotale
	#print "tauxAcceptation",tauxAcceptation
	return tauxAcceptation


######################################################
                
                            
                            
def toArff(contenuBaseSequence, mesAttributs, arffData, indiceClass, classAtt):
    for sequence in contenuBaseSequence:
        seq=sequence.split(' -1 ')
        for s in mesAttributs:
            if EstSousSequence(s,sequence,indiceClass)==True:
                arffData=arffData+"1,"
            else:
                arffData=arffData+"0,"
        arffData=arffData+"'"+seq[indiceClass]+"'"+'\n'
        classAtt.add(seq[indiceClass])           
    return [arffData, classAtt]
