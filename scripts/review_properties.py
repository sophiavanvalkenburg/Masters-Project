#!/usr/bin/python

import sys

fname = sys.argv[1]
file = open(fname)
curr_review = 0
num_features = 0
aggr_score = 0.0
lines = file.readlines()
for i in range(0,len(lines)):
    line = lines[i]
    cols = line.split(',')
    r_id = int(cols[0])
    score = float(cols[3])
    if (r_id == curr_review):
        num_features += 1
        aggr_score += score
        if i == len(lines)-1:
            print curr_review, num_features, abs(aggr_score/num_features)
    else:
        print curr_review, num_features, abs(aggr_score/num_features)
        curr_review = r_id
        num_features = 1
        aggr_score = score
        if i == len(lines)-1:
            print curr_review, num_features, abs(aggr_score/num_features)
