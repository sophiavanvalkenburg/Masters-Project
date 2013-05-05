#!/usr/bin/python

"""
note: seems to pick up long reviews and highly positive/negative reviews very well

"""


import sys
import math
import numpy as np
import create_data_matrix as cr

#round the values in the matrix to 10 decimal places. use to prevent rounding errors
round_matrix = np.vectorize(lambda x : round(x,10))

file = open(sys.argv[1])
double_cols = True if sys.argv[2] == "d" else False #if double_cols is true, then we have double columns for pos/neg features.
processing_type = 0
if sys.argv[3] == "raw": processing_type = 1
elif sys.argv[3] == "mean": processing_type = 2
elif sys.argv[3] == "norm": processing_type = 3
feature_matrix = cr.create_data_matrix(file.readlines(), double_cols,processing_type)
feature_matrix = round_matrix(feature_matrix)
U, s, Vt = np.linalg.svd(feature_matrix)
#k = cr.calculate_threshold(s,0.95)
k=int(sys.argv[4])
s[k+1:] = 0
S = np.zeros(shape=np.shape(feature_matrix))
S[:len(s),:len(s)] = np.diagflat(s)
normals = U * S * Vt
normals = round_matrix(normals)
resid = feature_matrix - normals
for r in resid:
    print math.pow(np.linalg.norm(r),2)
