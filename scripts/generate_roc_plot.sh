#!/bin/bash


input=$1        #file name prefix
date=$2
processing=$3   # [raw | mean | norm]
k=$4
cutoff=$5       #cutoff for normal / anomaly
direction="lt"    #less than or greater than threshold is normal
thresh_file=$6  #file containing threshold values

title=$7 #title of plot
output=$8 #plot picture file name

echo "generating roc curves for $input..."
./generate_roc.sh "$input.results-$date" d "$processing" "$k" "$cutoff" "$direction" "$thresh_file" > "$input.results-$date-roc-$processing-$k"
./generate_roc.sh "$input.tfidf-$date" s "$processing" "$k" "$cutoff" "$direction" "$thresh_file" > "$input.tfidf-$date-roc-$processing-$k"
./generate_roc.sh "$input.filtered-tfidf-$date" s "$processing" "$k" "$cutoff" "$direction" "$thresh_file" > "$input.filtered-tfidf-$date-roc-$processing-$k"

echo "plotting roc curve for $input..."
./roc_curve_plot.py "$output" "$title" "$input.results-$date-roc-$processing-$k" "opinion" "$input.tfidf-$date-roc-$processing-$k" "tf-idf" "$input.filtered-tfidf-$date-roc-$processing-$k" "filtered tf-idf"

