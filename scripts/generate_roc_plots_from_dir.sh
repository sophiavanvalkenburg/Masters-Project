#!/bin/bash

dir=$1
fname=$2
date=$3

cutoff=$4       #cutoff for normal / anomaly
thresh_file=$5  #file containing threshold values


./generate_roc_plot.sh "$dir$fname" "$date" "raw" 20 "$cutoff" "$thresh_file" "ROC curve for $fname, raw, k=20" "testplots/$fname-$date-roc-raw-20.png"
./generate_roc_plot.sh "$dir$fname" "$date" "mean" 20 "$cutoff" "$thresh_file" "ROC curve for $fname, mean, k=20" "testplots/$fname-$date-roc-mean-20.png"
./generate_roc_plot.sh "$dir$fname" "$date" "norm" 20 "$cutoff" "$thresh_file" "ROC curve for $fname, norm, k=20" "testplots/$fname-$date-roc-norm-20.png"
./generate_roc_plot.sh "$dir$fname" "$date" "raw" 10 "$cutoff" "$thresh_file" "ROC curve for $fname, raw, k=10" "testplots/$fname-$date-roc-raw-10.png"
./generate_roc_plot.sh "$dir$fname" "$date" "mean" 10 "$cutoff" "$thresh_file" "ROC curve for $fname, mean, k=10" "testplots/$fname-$date-roc-mean-10.png"
./generate_roc_plot.sh "$dir$fname" "$date" "norm" 10 "$cutoff" "$thresh_file" "ROC curve for $fname, norm, k=10" "testplots/$fname-$date-roc-norm-10.png"
./generate_roc_plot.sh "$dir$fname" "$date" "raw" 5 "$cutoff" "$thresh_file" "ROC curve for $fname, raw, k=5" "testplots/$fname-$date-roc-raw-5.png"
./generate_roc_plot.sh "$dir$fname" "$date" "mean" 5 "$cutoff" "$thresh_file" "ROC curve for $fname, mean, k=5" "testplots/$fname-$date-roc-mean-5.png"
./generate_roc_plot.sh "$dir$fname" "$date" "norm" 5 "$cutoff" "$thresh_file" "ROC curve for $fname, norm, k=5" "testplots/$fname-$date-roc-norm-5.png"

open testplots
