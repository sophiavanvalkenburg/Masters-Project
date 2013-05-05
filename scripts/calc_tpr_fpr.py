#!/usr/bin/python

import sys

test_index = int(sys.argv[1]) #after this index, reviews are considered anomalous
threshold = float(sys.argv[2]) #the threshold to test
threshold_greater = True if sys.argv[3] == "gt" else False

tp = 0 #true positive
tn = 0 #true negative
fp = 0 #false positive
fn = 0 #false negative
line_count = 0
for line in sys.stdin:
    line_count += 1
    score = float(line)
    hyp = 0
    ref = 0
    if line_count > test_index:
        ref = 1
#    print line_count,ref
    if (threshold_greater and score > threshold) or ( not threshold_greater and score <= threshold):
        hyp = 1
    if ref == 0 and hyp == 0:
        tn += 1
    elif ref == 1 and hyp == 1:
        tp += 1
    elif ref == 0 and hyp == 1:
        fp += 1
    else: #ref == 1 and hyp == 0
        fn += 1
print float(tp)/(tp+fn), ',', float(fp)/(fp+tn)
