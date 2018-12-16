#!C:\Python27
#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import sys
import math
import csv
import re
import random
from math import log
import time


#Norm of a sequence from its corresponding array of itemsets 
def normeTabItemset(tabItemset):
	sequence='-1 '.join(tabItemset).replace('-1 ', '').split()#[:-1]
	return len(sequence)

#Intersection of two itemsets
def intersection(itemset1,itemset2):
    itemset1=itemset1.split()#[:-1]
    itemset2=itemset2.split()#[:-1]
    itemset=[]
    for item in itemset1:
        if item in itemset2:
            itemset.append(item)
    return ' '.join(itemset)+' '

def intersection1(itemset1,itemset2):
    itemset1=itemset1.split()#[:-1]
    itemset2=itemset2.split()#[:-1]
    return ' '.join(list(set(itemset1).intersection(set(itemset2))))+' '

#Position set
def positionSet(sequence, itemset):
	ps,i=[], 0
	x=len(sequence)
	#print "sequence, itemset",sequence, itemset
	while i<x:
		intersec=intersection(sequence[i],itemset)
		if intersec !=' ':
			k,nL,chaine=i+1,len(ps), intersec
			while k < x and chaine not in intersection(sequence[k],itemset):
				k+=1
			if k==x:
				ps.append(i)
		i+=1
	return ps


#Set of all subset of a given set
def lamine(ens):
    p = []
    i, imax = 1, 2**len(ens)-1
    while i <= imax:
        s = []
        j, jmax = 0, int(log(i,2))
        while j <= jmax:
            if (i>>j)&1 == 1:
                s.append(ens[j])
            j += 1
        p.append(s)
        i += 1 
    return p

#sequence formed by the itemsets of the index of 0..k
def prefixe(sequence,k):
	return sequence[:-(len(sequence)-1-k)]


#Size of an itemset
def tailleItemset(itemset):
	return len(itemset.split(' ')[:-1])


def unionElem(positionSet,sequence):
	result=set()
	for f in positionSet:	
		result=result.union(set(sequence[f].split(' ')[:-1]))
	return result


def tableauItems(seq):
	tab=[]
	for f in seq:
		tab+=f.split(' ')[:-1]
	return tab

def prefix(seq,itemset):
	for f in seq:
		if itemset in f:
			return True
	return False



# A deprivate sequence of his last itemset
def moinsDernierItemset(sequence):
	return sequence[:-1]

def nbItems(itemset):
	return len(itemset.split(' ')[:-1])

# Number of sub-sequence of norm smaller or equal to k of a given sequence
def phi_k(sequence,k):
	if k==0 or sequence==[]:
		return [[1]]
	else:
		nt=normeTabItemset(sequence)
		k=min(k,nt)
		T=[[1],[1]]
		R=[[0],[0]]
		for i in range(1,k+1):
			T[0].append(1)
			T[1].append(T[1][i-1]+combin(nbItems(sequence[0]),i))
			R[0].append(0)
			R[1].append(0)
		for i in range(2,len(sequence)+1):
			nbI=nbItems(sequence[i-1])
			R.append([0])
			T.append([1])
			ps=positionSet(sequence[:i-1], sequence[i-1])
			sousEnsPS=lamine(ps)
			for j in range(1,k+1):
				T[i].append(int(0))
				R[i].append(int(0))
				for u in range(len(sousEnsPS)):
					intersecMulti=sequence[:i-1][sousEnsPS[u][0]]
					v=1
					while v<len(sousEnsPS[u]):
						intersecMulti=intersection(intersecMulti,sequence[:i-1][sousEnsPS[u][v]])
						v+=1
					intersecMulti=intersection(sequence[i-1],intersecMulti)
					if intersecMulti==' ':
						intersecMulti=''
					m = min(sousEnsPS[u])
					kmax = tailleItemset(intersecMulti)
					for v in range(1,j+1):
						R[i][j] += pow(-1,len(sousEnsPS[u])+1)*T[m][j-v]*combin(kmax,v)
				for v in range(min([tailleItemset(sequence[i-1]),j])+1):
					T[i][j] += T[i-1][j-v]*combin(tailleItemset(sequence[i-1]),v)
				T[i][j] -= R[i][j]
		return T

# number of subsequences (bis)
def phi_k_Bis(sequence,k):
	if k==0 or sequence==[]:
		return [[1]]
	else:
		M=[]
		nt=normeTabItemset(sequence)
		k=min(k,nt)
		#print(nt),(len(sequence))
		if nt==len(sequence):
			if nt==len(set(sequence)):
				return [[combin(nt,h) for h in xrange(k+1)]]
		nbItem=nbItems(sequence[0])
		T=[]
		for i in xrange(0,k+1):
			T.append(combin(nbItem,i))
		tab=list(T)
		n=len(sequence)
		M.append(T)
		for i in xrange(1,n):
			nbI=nbItems(sequence[i])
			for j in xrange(1,k+1):
				som=0
				for l in xrange(max(j-nbI,0),j):
					som+=M[i-1][l]*combin(nbI, j-l)
				#som-=correction(sequence[:i], sequence[i],M,j,i)
				tab[j]=som+M[i-1][j]-termeCorrecteurLDIOPBSF(M,sequence[:i], sequence[i],j) #-(termeCorrecteurBSF(sequence[:i], sequence[i],j) - termeCorrecteurBSF(sequence[:i], sequence[i],j-1))
			T=list(tab)
			M.append(T)
	return M

#the correction term
def termeCorrecteurLDIOPBSF(M,sequence, itemset,k):
	ps=positionSet(sequence, itemset)
	sousEnsPS=lamine(ps)
	#print(sousEnsPS)
	termCorrec,i=0,len(sousEnsPS)-1
	while i>=0:
		j=1
		intersecMulti=sequence[sousEnsPS[i][0]]
		while j<len(sousEnsPS[i]):
			intersecMulti=intersection(intersecMulti,sequence[sousEnsPS[i][j]])
			j+=1
		intersecMulti=intersection(itemset,intersecMulti)
		if intersecMulti==' ':
			intersecMulti=''
		val=0
		for l in range(k-1):
			x=1
			if min(sousEnsPS[i])>0: x=sum(M[min(sousEnsPS[i])-1][:l+1])
			val+=x*(combin(tailleItemset(intersecMulti),k-l)-combin(tailleItemset(intersecMulti),k-1-l))
		x=1
		if min(sousEnsPS[i])>0: x=sum(M[min(sousEnsPS[i])-1][:k])
		termCorrec+=pow(-1,len(sousEnsPS[i])+1)*(val+x*combin(tailleItemset(intersecMulti),1))
		i-=1
	return termCorrec

# Number of combinations of n objects taken k to k
def combin(n, k):
	"""Nombre de combinaisons de n objets pris k a k"""
	if k>n or n==0: return 0 #LDIOPBSF
	if k > n//2:
		k = n-k
	x = 1
	y = 1
	i = n-k+1
	while i <= n:
		x = (x*i)//y
		y += 1
		i += 1
	#print "x",x
	return x

# seq="574 -1 4 -1 1305 -1 1306 -1 1307 -1 1308 -1 1309 -1 690 -1 1360 -1 5979 -1 5980 -1 4968 -1 699 -1 "
# seq=seq.split("-1 ")[:-1]
# print(seq)
# tmps=time.clock()
# v=phi_k(seq, 7)
# tmps1=time.clock()-tmps
# print(v),(tmps1)



