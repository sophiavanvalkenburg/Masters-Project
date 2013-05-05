#!/bin/bash

file=$1         #file name to run the tests on
ds=$2           #[d]ouble or [s]single columns
cutoff=$3       #cutoff for normal / anomaly
direction=$4    #less than or greater than threshold is normal
c_alpha=$5      #1-alpha in standard normal distribution

norms=$(./anomaly_test.py "$file" "$ds")
threshold=$(./calc_threshold.py "$file" "$ds" "$c_alpha") 
echo "$norms" | ./calc_tpr_fpr.py "$cutoff" "$threshold" "$direction"
