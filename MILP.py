#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:46:05 2018

L: is a large number

overview is a 'number-of-jobs' x 2 array consisting of a list of operations and a list of machines for every job=row i

data is a dictionary of the form {(job_number, process_number, machine_number) : processing_time}, which carries the 
available data

prec is a list with entries of type ((job_num, proc_num, machine),(other job_num, other proc_num, same machine))

d is a list of job due dates

@author: marios
"""

from pulp import *
import numpy as np



jobs = range(1,len(overview)+1)

## -- problem  

prob = LpProblem("FJSSP", LpMinimize) 


## -- (decision) variables 

routing = LpVariable.dicts('routing', (i for i in data.keys()),0,1,LpBinary)

preced = LpVariable.dicts('different-job precedence', (i for i in prec),0,1,LpBinary)

delta = LpVariable("delta",None,None,LpContinuous)  # delta --> to be minimized

S = LpVariable.dicts("Starting Times",0,None,LpInteger) 

C = LpVariable.dicts("Completion time of process",0,None,LpInteger)

Comp = LpVariable.dicts("Job completion times",0,None,LpInteger)

## --- objective function ---

prob += delta

## --- constraints ---

#1  
for i in jobs:
    prob += Comp[i] - d[i] <= delta 

#2
for i in jobs:
    for j in overview[i][0]: # operations of job i
        prob += lpSum(routing[(i,j,k)] for k in overview[i][1]) == 1
        
#3
for i in jobs:
    for j in overview[i][0]: # operations of job i
        for k in overview[i][1]: # machines 
            prob += S[(i,j,k)]+C[(i,j,k)] <= routing[(i,j,k)]*L

#4
for i in jobs:
    for j in overview[i][0]: # operations of job i
        for k in overview[i][1]: # machines
            prob += C[(i,j,k)] >= S[(i,j,k)] + data[(i,j,k)] - (1 - routing[(i,j,k)])
#5


#6
for i in jobs:
    for j in overview[i][0]: # operations of job i
        prob += lpSum(S[(i,j,k)] for k in overview[i][1]) >= lpSum(C[i][j-1][k] for k in overview[i][1])
        
#7
for i in jobs:
    prob += lpSum(S[(i,j,k)] + data[(i,j,k)] for k in overview[i][1]) == Comp[i]
  
#8
for r in prec:
    prob += L*preced[r] + (C[r[0]] - C[r[1]]) <= 2*L 
