#!/usr/bin/python

import math
import numpy as np

RAW = 1
MEAN_CENTER = 2
UNIT_NORM = 3


def calculate_threshold(s,p):
    total = sum([math.pow(ss,2) for ss in s])
    count = 0
    k = 0
    for i in s:
        count += math.pow(i,2)
        k += 1
        if total*p <= count: break
    return k

def mean_center(m):
    means = np.mean(np.array(m), axis=0)
    mT = m.T.tolist()
    centered_matrix = []
    for i in range(0,len(mT)):
        row_i = mT[i]
        mean = means[i]
        centered_matrix.append([cell-mean for cell in row_i])
    return np.matrix(centered_matrix).T

def unit_norm(m):
    mT = m.T.tolist()
    normalized_matrix = []
    for row in mT:
        norm = np.linalg.norm(row)
        if norm == 0: normalized_matrix.append(row)
        else: normalized_matrix.append([cell/norm for cell in row])
    return np.matrix(normalized_matrix).T

def create_feature_dict(lines):
    feature_dict = {} # format: { "feature": [list of review ids that contain feature]}
    n_reviews = 0
    prev_review = -1
    for line in lines:
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
    return (feature_dict, n_reviews)

def create_reviews_list(feature_dict, n_reviews,double_cols):
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
    return reviews

def create_data_matrix(lines, double_cols,processing_type):
    feature_dict,n_reviews = create_feature_dict(lines)
    reviews = create_reviews_list(feature_dict, n_reviews, double_cols)
    if processing_type == MEAN_CENTER:
        return mean_center(np.matrix(reviews))
    elif processing_type == UNIT_NORM:
        return unit_norm(np.matrix(reviews))
    elif processing_type == RAW:
        return np.matrix(reviews)
    else:
        return np.matrix(reviews)
