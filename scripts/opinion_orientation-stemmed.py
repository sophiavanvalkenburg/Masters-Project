#!/bin/python

import re
import copy
from nltk.stem.lancaster import LancasterStemmer

#test_reviews = [[{"id":0,"text":[("this",DT), ("is",VB),("a",DT),("sentence",NN)], "features":[{"f1":(f1,0),"f2":(f2,0),"f3":(f3,0)], "opinion_words":{"opw1":(ow1,0),"opw2":(ow2,0)}]]

POSITIVE = 1
NEGATIVE = -1
NEUTRAL = 0

ADJ = 'JJ'
BUT_WORDS = ['but','however', 'in contrast', 'with the exception of', 'except for', 'except that']
NEG_WORDS = ['no', 'not', 'never']
NEG_ING_WORDS = ['stop','quit']
NEG_TO_WORDS = ['cease']

STEMMER = LancasterStemmer()

def opinion_orientation(reviews):
    """
    reviews: dictionary of reviews with features for each sentence
    
    determines opinion orientation of each feature in each sentence of each review
    
    returns: dictionary of reviews with (feature, opinion orientation) 
             pairs for each sentence
    """
    for review in reviews:
        for sentence in review:
            features = sentence['features']
            for feature,_ in features.values():
                update_orientation(sentence, feature)    
    #context dependent opinion words handling
    # note: seems like this doesn't really handle context-dependent *opinion words* -
    # rather it just handles features that have an orientation of 0.
        for sentence in review:
            features = sentence['features']
            for feature,_ in features.values():
                local_orientation = get_local_orientation(sentence, feature)
                if local_orientation == 0:
                    handle_context_dependency(review, sentence, feature)
    return reviews

def update_orientation(sentence, feature):
    """
    sentence: a particular sentence of a review
    feature:  a particular feature in the sentence
    
    determines the initial opinion orientation of the feature and updates the 
    sentence-level and global orientation for that feature
    
    returns:  nothing
    """
    orientation = 0
    if in_BUT_clause(sentence, feature):
        orientation = apply_BUT_rule(sentence, feature)
    else:
        sentence = remove_BUT_clause(sentence)
        for opw, marked in sentence['opinion_words'].values(): 
            if not marked:
                orientation += word_orientation(opw,feature,sentence)
    set_local_orientation(sentence, feature, orientation)
    global_orientation = get_global_orientation(feature)
    if is_adj(sentence,feature):
        set_global_orientation(feature, global_orientation \
                                        +get_local_orientation(sentence, feature))
    else:
        nearest_opw = find_nearest_opinion_word(sentence, feature)
        set_global_orientation(feature, global_orientation \
                                        +get_local_orientation(sentence, feature),\
                                        nearest_opw)
    
def handle_context_dependency(review, sentence, feature):
    """
    sentence: a particular sentence in a review
    feature:  a particular feature of the sentence

    if a feature was not assigned a polarity in the first runthrough,
    apply more rules to determine the orientation.

    returns: nothing
    """
    orientation = 0
    if is_adj(sentence,feature):
        orientation = get_global_orientation(feature)
        set_local_orientation(sentence, feature, orientation)
    else:
        orientation = apply_SYN_ANT_rule(sentence, feature)
        if orientation == 0: #syn_ant rule didn't do anything
            nearest_opw = find_nearest_opinion_word(sentence, feature)
            try:
                orientation = get_global_orientation(feature, nearest_opw)
                set_local_orientation(sentence, feature, orientation)
            except Error:
                #(feature,nearest_opw) pair doesn't exist
                pass
    if orientation == 0: #still neutral
        orientation = apply_INTER_SENTENCE_rule(review, sentence, feature)
        set_local_orientation(sentence, feature, orientation)

def word_orientation(opw, feature, sentence):
    """
    opw:      a given opinion word
    feature:  the feature whose orientation we will determine
    sentence: the sentence that contains the feature

    returns: orientation score for the opinion word that we will add
             to the aggregate score for the feature
    """
    orientation = 0
    if is_NEG(opw, sentence):
        orientation = apply_NEG_rule(opw, sentence)
    elif is_TOO(opw, sentence):
        orientation = apply_TOO_rule(opw, sentence)
    else:
        orientation = get_opinion_word_orientation(opw)
    return float(orientation)/distance(opw, feature, sentence)

def get_opinion_word_orientation(opw):
    return opw.orientation

def find_nearest_opinion_word(sentence, feature):
    """
    feature:  the feature whose orientation we will determine
    sentence: the sentence that contains the feature
    
    returns:  a string of the opinion word closest to the feature.
    """
    opwords = sentence['opinion_words']
    nearest_opw = None
    shortest_distance = float("Infinity")
    for opw,_ in opwords.values():
        dist = distance(opw, feature, sentence) 
        if dist < shortest_distance and dist > 0:
            shortest_distance = dist
            nearest_opw = opw
    return nearest_opw

def distance(opw, feature, sentence):
    """
    opw:      a given opinion word (string)
    feature:  a given feature (Feature)
    sentence: sentence that contains opw and feature

    returns:  the distance (in number of words) between the opinion word and the feature
    """
    # here I'm using the string name of the feature, which assumes
    # it is an explicit feature (it is specifically mentioned)
    # so this won't work for implicit features... needs fix.
    text_str = get_text_string(sentence['text'])
    feature_ind = text_str.find(STEMMER.stem(feature.name))
    opw_ind = text_str.find(opw.name)
    if feature_ind >= 0 and opw_ind >= 0:
        return abs(feature_ind-opw_ind)
    else: 
        return float("Infinity") 

def set_local_orientation(sentence, feature, orientation):
    if orientation > 0:
        orientation = POSITIVE
    elif orientation < 0:
        orientation = NEGATIVE
    features = sentence['features']
    features[feature.name] = (feature, orientation)

def set_global_orientation(feature, orientation, opw=None):
    if orientation > 0:
        orientation = POSITIVE
    elif orientation < 0:
        orientation = NEGATIVE
    if opw==None:
        feature.global_orientation['_default'] = orientation
    else:
        feature.global_orientation[opw.name] = orientation

def get_local_orientation(sentence, feature):
    features = sentence['features']
    try:
        _,orientation = features[feature.name]
        return orientation
    except KeyError:
        return 0

def get_global_orientation(feature, opw=None):
    try:
        if opw==None:
            return feature.global_orientation['_default']
        else:
            return feature.global_orientation[opw.name]
    except KeyError:
        return 0

def get_text_string(text):
    """
    text:    a sentence in (word, pos) format
    returns: all words concatenated to form a string (w/o pos) 
    """
    stemmed_text = [STEMMER.stem(t) for (t,_) in text]
    text_str = ""
    if len(stemmed_text) > 0: text_str = " ".join(stemmed_text)
    return text_str

def find_BUT_word(text_str):
    """
    text:    the sentence in (word, pos) form
    returns: the BUT word if it is in the text
    """
    for w in BUT_WORDS:
        w = STEMMER.stem(w)
        r = re.compile('(?!not only).*%s'%w)
        if r.match(text_str): return w
    return None

def find_NEG_words(text_str):
    """
    text:    the sentence in (word, pos) form
    returns: a list of negation words/phrases (strings) in text
    """
    neg_phrases = []
    for w in NEG_WORDS:
        w = STEMMER.stem(w)
        if re.match('%s (?!(just|only))'%w,text_str):
            neg_phrases.append(w)
    for w in NEG_ING_WORDS:
        w = STEMMER.stem(w)
        m = re.match('%s [a-z]+ing'%w,text_str) 
        if m:
            neg_phrases.extend(list(m.groups))
    for w in NEG_TO_WORDS:
        w = STEMMER.stem(w)
        m = re.match('%s to [a-z]+'%w, text_str)
        if m:
            neg_phrases.extend(list(m.groups))
    return neg_phrases

def is_adj(sentence,feature):
    text = sentence['text']
    for (word, pos) in text:
        if STEMMER.stem(word)==STEMMER.stem(feature.name) and pos==ADJ: return True
    return False

def in_BUT_clause(sentence, feature):
    """
    feature:  the feature that we want to determine is in a BUT clause or not
    sentence: the sentence that contains the feature

    returns:  true if feature is after a BUT word
    """
    text = sentence['text']
    text_str = get_text_string(text)
    BUT_word = find_BUT_word(text_str)
    if BUT_word==None: return False
    (s1,but,s2) = text_str.partition(BUT_word)
    if subset(s2,' '+feature.name+' '): return True
    else: return False
   
def apply_BUT_rule(sentence, feature):
    orientation = 0
    opwords = sentence['opinion_words']
    text = sentence['text']
    text_str = get_text_string(text)
    BUT_word = find_BUT_word(text_str)
    (s1, but, s2) = text_str.partition(BUT_word)
    for (opw, marked) in opwords.values(): 
        if subset(s1,' '+opw.name+' ') and not marked:
            orientation += word_orientation(opw, feature, sentence)
    if orientation != 0: return orientation
    #else still neutral, so we look at the first clause
    for (opw, marked) in opwords.values():
        if subset(s1,' '+opw.name+' ') and not marked:
            orientation += word_orientation(opw, feature, sentence)
    orientation *= -1
    return orientation

def remove_BUT_clause(sentence):
    """
    sentence: the sentence in which to remove the BUT clause
    returns:  a sentence with the BUT clause removed
    """
    #must copy to avoid messing up original sentence
    sentence_cpy = copy.copy(sentence) 
    text = copy.copy(sentence_cpy['text'])
    text_str = get_text_string(text)
    BUT_word = find_BUT_word(text_str)
    if BUT_word: 
        BUT_word_ind = text_str.find(BUT_word)
        del text[BUT_word_ind:]
        new_opwords = {}
        old_opwords = sentence['opinion_words']
        for opw_name in old_opwords:
            opw_ind = text_str.find(STEMMER.stem(opw_name))
            if opw_ind < BUT_word_ind:
               new_opwords[opw_name] = old_opwords[opw_name]
        sentence_cpy['opinion_words'] = new_opwords
        sentence_cpy['text'] = text
    return sentence_cpy

def apply_SYN_ANT_rule(sentence, feature):
    orientation = 0
    opwords = sentence['opinion_words']
    for opw,_ in opwords.values():
       #syn/ants lookup done in greedy fashion
        for s in opw.synonyms:
            orientation = get_global_orientation(feature, s)
            if orientation != 0: return orientation
        for a in opw.antonyms:
            orientation = get_global_orientation(feature, a)
            if orientation != 0: return orientation
    return 0
            

def apply_INTER_SENTENCE_rule(review, sentence,feature):
    """
    sentence: the current sentence
    review:   the review that contains the sentence

    returns: the orientation of the previous or next sentence
             if it exists
    """
    # note: in the original algorithm, I should find the orientation
    # of the *last clause* of the prev/next sentence. Here I simplify
    # it by just finding the orientation of the whole sentence, since
    # I have not built a good way to distiguish clauses.
    orientation = 0
    sentence_id = sentence['id']
    if sentence_id > 0:
        prev_sentence = review[sentence_id-1]
        orientation = get_local_orientation(prev_sentence,feature)#INTER_SENTENCE_rule_helper(prev_sentence,feature)
    if orientation == 0 and sentence_id+1 < len(review):
        next_sentence = review[sentence_id+1]
        orientation = get_local_orientation(next_sentence,feature)#INTER_SENTENCE_rule_helper(next_sentence,feature)
    return orientation
        
def INTER_SENTENCE_rule_helper(sentence, feature):
    """
    helper method for apply_INTER_SENTENCE_rule
    """
    # not quite sure what "orientation of the previous sentence" means.
    # here I just assume it is an aggregate of opinion word orientations
    text = sentence['text']
    orientation = 0
    for opw,marked in sentence['opinion_words'].values():
        if not marked:
            orientation += get_opinion_word_orientation(opw)
    return orientation

def is_NEG(opw, sentence):
    """
    opw:      a given opinion word
    sentence: the sentence that contains the opinion word

    returns:  true if opw is in a negative phrase, false otherwise
    """
    neg_phrases = find_NEG_words(get_text_string(sentence['text']))
    for neg_phrase in neg_phrases:
        if subset(neg_phrase,' '+opw.name+' '): return True
    return False

def apply_NEG_rule(opw, sentence):
    """
    opw:      a given opinion word
    sentence: the sentence that contains the opinion word

    returns:  the orientation of the negative phrase that
              contains the opinion word, according to the 
              negation rules
    """
    text = sentence['text']
    orientation = get_opinion_word_orientation(opw)
    neg_phrases = find_NEG_words(get_text_string(text))
    for neg_phrase in neg_phrases:
        if subset(neg_phrase,' '+opw.name+' '):
            sentence['opinion_words'][opw] = 1 #marked
            if orientation == 0: return -1
            else: return -1*orientation
    return 0

def subset(s1,s2):
    #assuming s1 has already been stemmed
    s2 = STEMMER.stem(s2)
    return s1.partition(s2)[1] == s2

"""
the following two methods are left unimplemented
"""
def is_TOO(opw, sentence):
    return False

def apply_TOO_rule(opw, sentence):
    #must also mark the opw in sentence
    return 0


