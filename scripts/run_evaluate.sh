#!/bin/bash

for file in $1*
do
    if [[ $file == *".txt"  && $file != *"Readme.txt" ]]
    then
        echo "evaluating $file..."
        echo ""
        ./evaluate.py -t "results/$file.results-$2" "$file.features"
        ./evaluate.py -p "results/$file.results-$2" "$file.features"
        ./evaluate.py -n "results/$file.results-$2" "$file.features"
    fi
done
