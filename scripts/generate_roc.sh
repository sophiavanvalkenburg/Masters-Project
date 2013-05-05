#!/bin/bash

file=$1         #file name to run the tests on
ds=$2           #[d]ouble or [s]single columns
processing=$3   #[ raw | mean | norm ]
k=$4            #knee
cutoff=$5       #cutoff for normal / anomaly
direction=$6    #less than or greater than threshold is normal
thresh_file=$7  #file containing threshold values

norms=$(./anomaly_test.py "$file" "$ds" "$processing" "$k")

for threshold in $(cat "$thresh_file")
do 
    echo "$norms" | ./calc_tpr_fpr.py "$cutoff" "$threshold" "$direction"
done
