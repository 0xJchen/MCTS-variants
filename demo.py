import numpy as np
import random
import time

def pi_a(pi,q,a,multiplier):
    return multiplier*pi/(a-q)

def dichotomic_search(arr,l,r,multiplier,pi,q,error_bound):
    while l<r:
        m=(l+r)//2
        policy_sum=pi_a(pi,q,arr[m],multiplier).sum()
        err=np.abs(policy_sum-1)
        if err<=error_bound:
            return arr[m], err
        elif policy_sum>(1-error_bound):
            l=m+1
        else:
            r=m
    return -1

action_num=20
c=1.25

pi=np.array([random.random() for _ in range(action_num)])
pi=np.exp(pi)/sum(np.exp(pi))

q=np.array([random.random() for _ in range(action_num)])
q=(q-q.min())/(q.max()-q.min())

# budget=[10,50,100]
budget=[10]
accuracy=1000
error_bound=0.01

for simulation_budget in budget:
    t1=time.time()
    multiplier=c*np.sqrt(simulation_budget)/(action_num+simulation_budget)

    min_a=(q+multiplier*pi).max()
    max_a=q.max()+multiplier


    a_range=np.linspace(min_a,max_a,num=accuracy)

    assert ((multiplier*pi/(min_a-q)).sum())>=1

    found_a,err=dichotomic_search(a_range,0,len(a_range),multiplier,pi,q,error_bound)
    print("simulation={}, multiplier={}, min_a={}, min_sum={}, max_a={}, max_a_sum={} found_a={} in {} s with error={}".format(simulation_budget,multiplier,min_a,pi_a(pi,q,min_a,multiplier).sum(),max_a,pi_a(pi,q,max_a,multiplier).sum(),found_a,time.time()-t1,err))
