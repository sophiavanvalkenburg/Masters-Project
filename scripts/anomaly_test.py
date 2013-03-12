#!/usr/bin/python

"""
note: seems to pick up long reviews and highly positive/negative reviews very well

"""


import sys
import math
import numpy as np

def calculate_threshold(s,p):
    total = sum(s)
    count = 0
    k = 0
    for i in s:
        count += i
        k += 1
        if total*p <= count: break
    return k

file = open(sys.argv[1])
double_cols = True if sys.argv[2] == "d" else False #if double_cols is true, then we have double columns for pos/neg features.
feature_dict = {} # format: { "feature": [list of review ids that contain feature]}
n_reviews = 0
prev_review = -1
for line in file:
    cols = line.split(',')
    review_id = int(cols[0])
    if prev_review != review_id: #add room for the review in the review array
        prev_review = review_id
        n_reviews += 1
    feature = cols[2]
    opinion = float(cols[3])
    if feature not in feature_dict:
        feature_dict[feature] = []
    feature_dict[feature].append((n_reviews-1,opinion)) #use n_reviews as index because some reviews will be skipped if they have no features
feature_vals = feature_dict.values()
reviews = []
for i in range(0,n_reviews):
    r = [0]*2*len(feature_vals) if double_cols else [0]*len(feature_vals) #two columns each for pos/neg opinion
    reviews.append(r)
for i in range(0, len(feature_vals)):
    occurs_in = feature_vals[i]
    f_ind = 2*i if double_cols else i
    for (index, opinion) in occurs_in:
        if opinion > 0 or not double_cols:
            reviews[index][f_ind] = opinion
        elif opinion < 0:
            reviews[index][f_ind+1] = abs(opinion)
        #if opinion > 0:
        #    reviews[review_id][f_ind] = 1
        #elif opinion < 0:
        #    reviews[review_id][f_ind+1] = 1
feature_matrix = np.matrix(reviews)
U, s, Vt = np.linalg.svd(feature_matrix)
k = calculate_threshold(s,0.95)
S = np.diagflat(s[:k])
U_ = U[:,:k]
Vt_ = Vt[:k,:]
normals = U_ * S * Vt_
resid = feature_matrix - normals
for r in resid:
    print np.linalg.norm(r)
