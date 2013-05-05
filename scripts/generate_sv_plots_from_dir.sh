#!/bin/bash

dir=$1
name=$2

for file in "$dir"*
do
    if [[ $file == *"results"* && $file != *"sv"* ]]
    then
        fname=${file#$dir}
        ./generate_sv_plot.sh "$file" d "Singular Values for $fname" "testplots/$name$fname-sv.png"
    elif [[ $file == *"tfidf"* && $file != *"sv"* ]]
    then
        fname=${file#$dir}
        ./generate_sv_plot.sh "$file" s "Singular Values for $fname" "testplots/$name$fname-sv.png"
    fi
done

open testplots
