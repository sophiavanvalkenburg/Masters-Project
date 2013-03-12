#!/usr/bin/python

import sys
import numpy as np

file = open(sys.argv[1])
feature_dict = {} # format: { "feature": [list of review ids that contain feature]}
n_reviews = 0
for line in file:
    cols = line.split(',')
    review_id = int(cols[0])
    if n_reviews < review_id+1: #add room for the review in the review array
        n_reviews += 1
    feature = cols[2]
    opinion = float(cols[3])
    if feature not in feature_dict:
        feature_dict[feature] = []
    feature_dict[feature].append((review_id,opinion))
feature_vals = feature_dict.values()
reviews = []
for i in range(0,n_reviews):
    r = [0]*2*len(feature_vals) #two columns each for pos/neg opinion
    reviews.append(r)
for i in range(0, len(feature_vals)):
    occurs_in = feature_vals[i]
    f_ind = 2*i
    for (review_id, opinion) in occurs_in:
        if opinion > 0:
            reviews[review_id][f_ind] = opinion
        elif opinion < 0:
            reviews[review_id][f_ind+1] = opinion
        #if opinion > 0:
        #    reviews[review_id][f_ind] = 1
        #elif opinion < 0:
        #    reviews[review_id][f_ind+1] = 1
feature_matrix = np.matrix(reviews)
U, s, V = np.linalg.svd(feature_matrix)
for val in s:
    print val
print "TOTAL REVIEWS:",len(reviews)
