#!/usr/bin/python

"""
a program for testing opinion_files_parser.py and opinion_orientation.py
"""

import sys
import opinion_files_parser as op
import opinion_orientation as oo

fnames = {'reviews':sys.argv[1], 'features':sys.argv[2],'pos_opwords':sys.argv[3],'neg_opwords':sys.argv[4]}
real = True if sys.argv[5] == 'r' else False
reviews = oo.opinion_orientation(op.parse_opinion_files(fnames),real)


for i in range(0,len(reviews)):
    review = reviews[i]
    for j in range(0,len(review)):
        sentence = review[j]
        #print oo.get_text_string(sentence['text'])
        features =  sentence['features']
        for f in features:
            print i,",",j,",",features[f][0].name,",",features[f][1]
            #print features[f][0].name,":",features[f][1]
