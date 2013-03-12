#!/bin/bash

for file in $1*
do
    if [[ $file == *".txt"  && $file != *"Readme.txt" ]]
    then
        echo "performing opinion extraction on $file..."
        ./opinion_test.py "$file.reviews" "$file.features" opinion-lexicon-English/test.poswords opinion-lexicon-English/test.negwords > "results/$file.results-$2"
    fi
done
