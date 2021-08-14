#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
from epanettools import epanet2 as et
from epanettools.examples import simple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from tqdm import tqdm

file = os.path.join(os.path.dirname(simple.__file__),'Austin_Pattern.inp')

ret=et.ENopen(file,"Austin_Pattern.rpt","")

# Network Properties
ret,nlinks=et.ENgetcount(et.EN_LINKCOUNT)
ret,nnodes=et.ENgetcount(et.EN_NODECOUNT)

nodes=[]
links=[]

for index in range(1,nnodes+1):
    ret,t=et.ENgetnodeid(index)
    nodes.append(t)

for index in range(1,nlinks+1):
    ret,t=et.ENgetlinkid(index)
    links.append(t)    
    
pumps=[91,92,93,94,95,96,97]
npumps=len(pumps)

import itertools
status=list(itertools.product(([0, 1]), repeat=npumps))

for x in status:
    if sum(x)>5:
        status.remove(x)
status.remove((1,1,1,1,1,1,0))
#이건 왜 안지워지는지 모르겠음
status.remove((1,1,1,0,0,1,1))
status.remove((1,1,0,1,0,1,1))
status.remove((1,1,0,0,1,1,1))
status.remove((0,0,1,1,1,1,1))

ncase=len(status)

pres_init=[]
for i in range(0,ncase):
    t=[]
    pres_init.append(t)
    for j in range(nnodes):
        y=[]
        pres_init[i].append(y)

time=[]
for i in range(ncase):
    t=[]
    time.append(t)
    
et.ENsettimeparam(et.EN_DURATION, 0)

for j in range(ncase):
    for k in range(npumps):
        et.ENsetlinkvalue(pumps[k], et.EN_INITSTATUS, status[j][k])
    
    et.ENopenH()
    et.ENinitH(0)

    while True:
        ret,t=et.ENrunH()
            
        for i in range(nnodes):
            ret,p=et.ENgetnodevalue(i+1, et.EN_PRESSURE)
            pres_init[j][i].append(p)

        ret,tstep=et.ENnextH()
        if (tstep<=0):
            break

    ret=et.ENcloseH()

init_40_evaluation=[]
for i in range(ncase):
    t=[]
    init_40_evaluation.append(t)

for i in range(ncase):
    for j in range(nnodes):
        if pres_init[i][j][0]>40:
            init_40_evaluation[i].append(1)

optimal_init_status=[]

for i in range(ncase):
    if sum(init_40_evaluation[i])==125:
        optimal_init_status.append(i+1)
        
print(optimal_init_status)
print(pres_init[3])

