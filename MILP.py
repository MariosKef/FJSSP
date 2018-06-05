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

L = 10**12
d = [1000]*10

jobs = range(1,len(overview)+1)

## -- problem  

prob = LpProblem("FJSSP", LpMinimize) 


## -- (decision) variables 

routing = LpVariable.dicts('routing', (i for i in data.keys()),0,1,LpBinary)

preced = LpVariable.dicts('different job precedence', (i for i in prec),0, 1, LpBinary)

delta = LpVariable("delta",None,None, LpContinuous)  # delta --> to be minimized

S = LpVariable.dicts("Starting Times",(i for i in data.keys()), 0,None,LpContinuous) 

C = LpVariable.dicts("Completion time of process",(i for i in data.keys()),0,None,LpContinuous)

Comp = LpVariable.dicts("Job completion times",range(1,len(overview)+1), 0,None,LpContinuous)

## --- objective function ---

prob += delta

## --- constraints ---

# new constraint  
for i in jobs:
    prob += Comp[i] - d[i-1] <= delta 


# each machine is assigned only one operation
for i in jobs:
    for j in overview[i-1][0]: # operations of job i
        prob += lpSum(routing[(i,j,k)] for k in overview[i-1][1]) == 1
        

# if an operation is not assigned to a machine S and C for that operation are set to 0
for key in data.keys():
    prob += routing[key]*L >= S[key] + C[key] 


# completion time of operation
for key in data.keys():
    prob += C[key] >= S[key] + data[key] - (1 - routing[key]) * L
        

# operation precedence
for i in jobs:
    for j in overview[i-1][0]: # operations of job i
        if j > 1:
            prob += lpSum(S[(i,j,k)] for k in overview[i-1][1]) >= lpSum(C[(i,j-1,k)] for k in overview[i-1][1])
        
# Compeletion time of job i definition
for i in jobs:
    j = overview[i-1][0][-1]
    prob +=  Comp[i] == lpSum(C[(i,j,k)] for k in overview[i-1][1])  
  
# different-job precedence on same machine, condition
for r in prec:
    prob += L*preced[r] + (C[r[0]] - C[r[1]]) <= 2*L 
