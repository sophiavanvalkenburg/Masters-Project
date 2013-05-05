#!/usr/bin/python


import sys
import math
import numpy as np
import create_data_matrix as cr

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
for ss in s:
    print ss
