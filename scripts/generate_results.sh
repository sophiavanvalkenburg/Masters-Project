#!/bin/bash

output=$1
d=$2
maj=$3
maj_range=$4
min=$5
min_range=$6

echo "Splicing $maj and $min reviews"
./splice_data.py "$maj.reviews" "$maj_range" "$min.reviews" "$min_range" > "$output.reviews"
echo "Splicing $maj and $min features"
./splice_data.py "$maj.features" "$maj_range" "$min.features" "$min_range" > "$output.features"
echo "running opinion extraction on $output"
./opinion_test.py "$output.reviews" "$output.features" opinion-lexicon-English/test.poswords opinion-lexicon-English/test.negwords r > "$output.results-$d"
echo "running tfidf on $output"
./tfidf.py "$output.reviews" > "$output.tfidf-$d"
echo "filtering tfidf features of $output"
./filter_features.py "$output.tfidf-$d" "$output.features" > "$output.filtered-tfidf-$d"
