#!/usr/bin/python

import sys
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

PUNCTUATION = ['.',',','?','~','!','(',')','*','-','_','{','}','[',']','\\',':',';','\'','"','<','>','/']
#STOP_WORDS = ['the','a','an','it','they','he','i','she','you','in','of','on','for','s','my','your','their','yours','theirs','us','to','is','are','am','be','im','and']
STOP_WORDS = stopwords.words('english')


fname = sys.argv[1]
file = open(fname)

stemmer = LancasterStemmer() 

"""
pre-process the text
"""
def text_helper(text):
    text = text.strip('\n')
    for p in PUNCTUATION:
        text = text.replace(p,'')
    new_text = ""
    words = text.split(' ')
    for w in words:
        if w in STOP_WORDS: continue
        new_text += stemmer.stem(w) + ' '
    return new_text

"""
td-idf
"""
def tf(word,review): return review.count(word)
def idf(word, reviews):
    count = 0
    for r in reviews.values():
        if word in r: count += 1
    return 1/float(count) if count != 0 else 0

"""
read in the data
"""
reviews = {} # id : text
lines = file.readlines()
for l in lines:
    cols = l.split(',')
    r_id = int(cols[0])
    text = text_helper(cols[2])
    if r_id not in reviews:
        reviews[r_id] = ""
    reviews[r_id] += text

"""
compute tf-idf for each word
"""
all_words = {}
for r_id in reviews:
    text = reviews[r_id]
    words = {}
    for w in text.split(' '):
        w = w.strip()
        if w != '' and w not in words:
            tf_val = tf(w,text)
            idf_val = idf(w,reviews)
            words[w] = tf_val*idf_val
    all_words[r_id] = words

for r_id in all_words:
    words = all_words[r_id]
    for w in words:
        print r_id, ',' ,0,',', w, ',' , words[w] #put 0 for sentence id because we don't need it
