# https://github.com/TeamErlich/dna-fountain/blob/master/robust_solition.pyx
# https://en.wikipedia.org/wiki/Soliton_distribution
# https://github.com/Spriteware/lt-codes-python/blob/master/distributions.py

import math
import numpy as np

def rho_d(K):
    rho = [1 / K]
    rho += [1 / (d * (d - 1)) for d in range(2, K+1)]
    return rho

def tau_d(K):   
    c = 0.2
    delta = 0.05
    
    S = c*math.log(K/delta)*math.sqrt(K)
    tau = []

    for d in range(1, K+1):
        if d <= math.floor((K/S) - 1):
            t = (S/K)*(1/d)
        elif d == math.floor(K/S):
            t = (S/K)*math.log(S/delta)
        elif d > math.floor(K/S):
            t = 0
        tau.append(t)
    return tau

def compute_Z(rho, tau):
    Z = 0
    for i in range(len(rho)):
        Z += rho[i]+tau[i]
    return(Z)

def mu_d(rho, tau, Z): 
    mu = []
    mu += [(rho[d]+tau[d])/Z for d in range(len(rho))]
    return mu
    
def probabilities(K):
    rho = rho_d(K)
    tau = tau_d(K)
    Z = compute_Z(rho,tau)
    mu = mu_d(rho,tau, Z)
    return mu 

# UNCOMMENT CODE BELOW IF YOU WANT TO SEE THE PROBABILITIES
    count = 1
    for p in mu:
##        print(count, p)
        count += 1
