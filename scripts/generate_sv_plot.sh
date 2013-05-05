#!/bin/bash

input=$1 #file containing opinion extraction results
d=$2 #double or single columns
title=$3 #title of plot
output=$4 #plot picture file name

echo "generating singular values for $input..."
./singular_vals.py "$input" "$d" "raw" > "$input-sv-raw"
./singular_vals.py "$input" "$d" "mean" > "$input-sv-mean"
./singular_vals.py "$input" "$d" "norm" > "$input-sv-norm"

echo "plotting singular values for $input..."
./singular_vals_plot.py "$output" "$title" "$input-sv-raw" "raw" "$input-sv-mean" "mean" "$input-sv-norm" "norm"

