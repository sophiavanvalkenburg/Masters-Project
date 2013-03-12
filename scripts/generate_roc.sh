#!/bin/bash

file=$1         #file name to run the tests on
ds=$2           #[d]ouble or [s]single columns
cutoff=$3       #cutoff for normal / anomaly
direction=$4    #less than or greater than threshold is normal
thresh_file=$5  #file containing threshold values

norms=$(./anomaly_test.py "$file" "$ds")

for threshold in $(cat "$thresh_file")
do 
    echo "$norms" | ./calc_tpr_fpr.py "$cutoff" "$threshold" "$direction"
done
