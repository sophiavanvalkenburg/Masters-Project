#!/bin/bash

rm $3
for file in ./$1*
do
    if [[ "$file" == *".results-$2" ]]
    then
        cat "$file" >> $3
        echo '#' >> $3
    fi
done
