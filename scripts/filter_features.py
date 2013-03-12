#!/usr/bin/python

"""
This script takes tf-idf results and filters just those that are included in the review's feature list
"""

import sys
from nltk import LancasterStemmer

tfidf_fname = sys.argv[1]
features_fname = sys.argv[2]
tfidf_file = open(tfidf_fname)
features_file = open(features_fname)

stemmer = LancasterStemmer() 

stemmed_features = []
for line in features_file:
    cols = line.split(',')
    feature = cols[2]
    stemmed_words = [stemmer.stem(w) for w in feature.split()]
    stemmed_features += stemmed_words

#print stemmed_features

for line in tfidf_file:
    cols = line.split(',')
    word = cols[2]
    if word.strip() in stemmed_features:
        print line.strip()
