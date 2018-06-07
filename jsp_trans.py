#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:52:55 2018

This script transforms the job scheduling data


@author: marios
"""

import copy
import numpy as np
import re
import itertools

m = 0
sch = []
avail_machines = []
with open('/home/marios/Desktop/LIACS-CIMPLO Project/Data/Benchmark/Job_Data/Brandimarte_Data/Text/Mk01.fjs') as f:
   for i,line in enumerate(f):

       if i>=1:
           line = line.rstrip().replace(' ','')
           print(line)
           k=1
           temp = []
           temp4 = []
           proc=1
           while k<len(line):
               temp2=[]
               temp3=[]
               x = int(line[k])
               
               for j in range(1,(2*x+1),2):
                   temp2.append((i, proc, int(line[k+j]),int(line[k+j+1])))
                   temp3.append(int(line[k+j]))
               proc = proc + 1
               k=k+j+2
               temp.append(temp2)
               temp4.append(temp3)
           sch.append(temp)
           avail_machines.append(temp4)
       else:
            line = line.rstrip().replace(' ','')
            m = int(re.sub(r'\t','',line)[2])
            

n = len(sch)
#for i in range(n):
##    flat = [item for sublist in sch[i] for item in sublist]
##    temp = []
##    for j in range(len(flat)):
##        temp.append(flat[j][0])
##    m = max(temp)
#    
#    c = len(sch[i])
#    for j in range(c):
#        if len(sch[i][j]) < m:
#            q=[]
#            for k in range(len(sch[i][j])):
#                q.append(sch[i][j][k][2])
#            diff = list(set(range(1,m+1)) - set(q))
#            for r in diff:
#                sch[i][j].append((i+1, sch[i][j][k][1], r, 10**6))
                
for i in range(n):
    m = len(sch[i])
    for j in range(m):
        sch[i][j].sort(key=lambda tup: tup[2])

temp = [item for sublist in sch for item in sublist]
process_times = [item for sublist in temp for item in sublist]
machines = [item for sublist in avail_machines for item in sublist]

temp = []
for x in process_times:
    temp.append(list(x))

print len(temp), len(machines)

data = {}

for entry in temp:
    z = entry.pop()
    data[tuple(entry)] = z

data2 = {}
for entry in temp:
    z = entry.pop()
    data2[tuple(entry)] = None

k = 0
for  entry in sorted(data2.iterkeys()):
    data2[entry] = machines[k]
    k+=1

        
overview=[]
for i in range(n):
    overview.append((range(1,len(sch[i])+1), range(1,m+1)))
    

        

# --- generating ((jobi,operij,k),(jobs,opersd,k))
jobs = list(itertools.combinations(range(1,n+1), 2))

D = []
for k in range(1,m+1):
    for cb in jobs:
        temp = list(itertools.product(overview[cb[0]-1][0],overview[cb[1]-1][0]))
        for r in temp:
            D.append(((cb[0],r[0],k),(cb[1],r[1],k)))
prec = []
for entry in D:
    if entry[0] in data.keys() and entry[1] in data.keys():
        prec.append(entry)
