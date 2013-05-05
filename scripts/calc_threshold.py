#!/usr/bin/python

import sys
import math
import numpy as np
import create_data_matrix as cr

def calc_lambda(s,j):
    return math.pow(s[j],2);

def calc_phi(r,m,s,i):
    sum = 0
    for j in range(r, m):
        sum += math.pow(calc_lambda(s,j),i)
    return sum

def calc_h0(phi1,phi2,phi3):
    return 1 - (2*phi1*phi3)/(3*math.pow(phi2,2))

round_matrix = np.vectorize(lambda x : round(x,10))

file = open(sys.argv[1])
double_cols = True if sys.argv[2] == "d" else False #if double_cols is true, then we have double columns for pos/neg features.
c_alpha = float(sys.argv[3])
feature_matrix = cr.create_data_matrix(file.readlines(), double_cols)
feature_matrix = round_matrix(feature_matrix)
U, s, Vt = np.linalg.svd(feature_matrix)
r = cr.calculate_threshold(s,0.95)
m = len(s)
phi1 = calc_phi(r,m,s,1)
phi2 = calc_phi(r,m,s,2)
phi3 = calc_phi(r,m,s,3)
h0 = calc_h0(phi1,phi2,phi3)
delta_sq = math.pow(phi1*( c_alpha*math.sqrt(2*phi2*math.pow(h0,2))/phi1 + 1 + phi2*h0*(h0-1)/math.pow(phi1,2) ),1/h0)

print delta_sq
