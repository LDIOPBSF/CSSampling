#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import time
import sys
import math
import csv
import re
import random
import functools
from pkg.cssamping.subSequence.SubSequence import *
from pkg.cssamping.preprocessing.LoadDataset import *
from pkg.cssamping.preprocessing.WeightedDataset import *
from pkg.cssamping.elementaryfunctions.Functions import *


def main():
    tailleMax = 3 # maximal norm, by default minimal norm m=1
    indiceClass = -1 # negative value if no class
    N=10000 # Sample size
    datasets = ["D10K5S2T6I.txt", "D10K6S3T10I.txt", "BMS.txt", "SIGN.txt", "D100K5S2T6I.txt", "D100K6S2T6I.txt"]
    for baseSequence in datasets:
        contenuBaseSequence = LoadDataset("Data\\"+baseSequence, -1).dataset
        relation=baseSequence.split(".")[0]
        print(relation)
        for tailleMax in [1,2,3,5,7,10]:
            print("M = ",tailleMax)
            for utility in ["freq"]:
                tmps1=time.process_time()
                print("utility",utility)
            #************  Preprocessing
                tmps21=time.process_time()
                wData = WeightedDataset(contenuBaseSequence,tailleMax,indiceClass,utility)
                basePonderee,tabSigma=wData.basePonderee,wData.tabSigma
                tmps22=time.process_time()-tmps21
                print ("Preprocessing time = ", tmps22)
            #************  Sampling
                for nbRep in range(1):
                    tmps21=time.process_time()
                    EnsSousSequence, EnsSequence=[],{}
                    nombreDeRejet,c_accept, c_rejet=0,0,0
                    tableauPhiSequence,tableauNbApparitionSequence=[],[]
                    i=0
                    while i<N:
                        mesValParam=SubSequence(EnsSequence, EnsSousSequence,nombreDeRejet,contenuBaseSequence,basePonderee, c_accept, c_rejet,tabSigma,indiceClass,utility)
                        nombreDeRejet,c_accept, c_rejet=mesValParam.nombreDeRejet,mesValParam.c_accept,mesValParam.c_rejet
                        i+=1
                    tmps22=time.process_time()-tmps21
                    print ("Sampling time = ", tmps22)
                #************  Ouput 
                #   creatArffFile(contenuBaseSequence, EnsSousSequence, indiceClass,relation,N,tailleMax,nbRep,utility)
                    recordSample(EnsSousSequence, N, tailleMax, utility, relation)
                #   recordSampleWithFrequecy(contenuBaseSequence, EnsSousSequence, N, tailleMax, utility, relation)
                tmps2=time.process_time()-tmps1
                print ("################## Total execution time = ",tmps2)
    
if __name__ == "__main__":
    main()

