#!/bin/bash

for file in "$1"*
do
    if [[ "$file" == *".txt" && "$file" != *"Readme.txt" ]]
    then
        echo "calculating singular values for $file"
        ./singular_vals.py "results/$file.results-$2" > "results/$file.sv-$2"
    fi
done
