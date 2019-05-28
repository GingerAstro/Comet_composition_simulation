from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import random
import math
import os
import numpy as np
import pandas as pd
import timeit
from decimal import Decimal

## setting initial variables for simulation
a=0.001 # Acceleration in Z ddirection
w=90 # Used in the spherical coordinates conversion
v1=0.85 # H20 -  Cockhran 1993 Velocity of parent molecule
v2=1.05 # OH - Cockhran 1993 # (1.2 km/s) Combi 1988b
tau_p=5.2E4 # H2O - Cochran 1993 lifetime of parent molecule
tau_d=1.6E5 # OH - Cochran 1993 lifetime of daughter molecule
tf=(tau_p+tau_d)*7 # test to see if this could be reduced

## cycle size and total molecules for simulation
## total melocules will be 'molecules_per_cycle * cycles_to_perform'
molecules_per_cycle = 10000000
cycles_to_perform = 10
threads_to_use = 5

## function to carry out calculations
def function1(x):
    yf,xf_prime = (0,0)
    ti=tf*random.random()
    phi1=2.0*np.pi*random.random()
    theta1=math.acos(1-2*random.random())
    phi2=2.0*np.pi*random.random()
    theta2=math.acos(1-2*random.random())
    td=ti-tau_p*math.log(random.random())
    tg=td-tau_d*math.log(random.random())
    t=0
    step=5000000
    #if x%step == 0 and x!=0: # used to keep track of progress
        #print 'molecule number', x

    if tg < tf: # Lost molecules
        t=0
        return t,yf,xf_prime

    if ((td)<tf and tg > tf): # daughter molecules
        t=2
        xf=(v1*(tf-ti)*math.sin(theta1)*math.sin(phi1))+(v2*(tf-td)*math.sin(theta2)*math.sin(phi2))
        yf=(v1*(tf-ti)*math.sin(theta1)*math.cos(phi1))+(v2*(tf-td)*math.sin(theta2)*math.cos(phi2))
        zf=(v1*(tf-ti)*math.cos(theta1))+(v2*(tf-td)*math.cos(theta2))-((a/2)*(tf-td)**2)
        xf_prime=xf*math.cos(math.radians(w))-zf*math.sin(math.radians(w))

        return t,yf,xf_prime

    if (td>tf and tg > tf): # parent molecules - if only daughter needed, comment out xf,yf,zf and xf_prime
        t=1
        xf=(v1*(tf-ti)*math.sin(theta1)*math.sin(phi1))+(v2*(tf-td)*math.sin(theta2)*math.sin(phi2))
        yf=(v1*(tf-ti)*math.sin(theta1)*math.cos(phi1))+(v2*(tf-td)*math.sin(theta2)*math.cos(phi2))
        zf=(v1*(tf-ti)*math.cos(theta1))+(v2*(tf-td)*math.cos(theta2))-((a/2)*(tf-td)**2)
        xf_prime=xf*math.cos(math.radians(w))-zf*math.sin(math.radians(w))

        return t,yf,xf_prime
                ###############################
                ######  End of function  ######
                ###############################

start = timeit.default_timer()
simstart = timeit.default_timer()
cycle_count=0

while cycle_count<cycles_to_perform:
    start = timeit.default_timer()
    print 'starting cycle',cycle_count+1

    data=range(int(molecules_per_cycle))
    pool = Pool(processes=threads_to_use)
    results2=filter(lambda a:a[1] !=0.0, pool.map(function1, data))
    pool.close()
    pool.join()
    cycle_count=cycle_count+1

    stop = timeit.default_timer()
    print 'cycle', cycle_count, 'finished, creating dataframe'
    df=pd.DataFrame(results2, columns=['t','y','xf_prime'])
    df.to_csv("df"+str(cycle_count)+".csv")
    results2 = 0
    df=0
    print 'cycle', cycle_count, 'run time:', stop - start

### joining dataframes into one
print 'joining dataframes'
start = timeit.default_timer()
frame = pd.DataFrame()
list_ = []
for file_ in range(int(cycles_to_perform)):
    filenum=file_+1
    df = pd.read_csv("df"+str(filenum)+".csv",index_col=None, header=0, names=['t','y','xf_prime'])
    list_.append(df)
    os.remove("df"+str(filenum)+".csv")

results = pd.concat(list_).reset_index(drop=True)

results.to_csv('final_results.csv')

print 'time to join dataframes', timeit.default_timer()-start
print 'simulation finished, time taken', timeit.default_timer()-simstart
