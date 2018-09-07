#!C:\Python27
#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import sys
import math
import csv
import re
import time


tmps1=time.clock()

delimiteurItemset='-1'

# Transform the sequence into an array of itemsets
def tableauItemset(sequence):
	sequence=sequence[:-3]
	return sequence.split(delimiteurItemset+' ')
