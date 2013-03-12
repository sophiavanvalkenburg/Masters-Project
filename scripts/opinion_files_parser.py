#!/usr/bin/python

"""
opinion_files_parser.py

converts files into correct python data structures for use
in opinion_orientation.py

inputs: review file (review_id,sentence_id, text)
        postive opinion word file (one word per line)
        negative opinion word file (one word per line)
        feature file (review_id,sentence_id, text)

output: list of reviews  with the following data structure:
        review = [sentence]
        sentence = {"id":int, "text":[(string(word), string(POS))],
                    "features":{"feature_name":(Feature, int(orientation))},
                    "opinion_words":{"word_name":(OpinionWord, int(marked)}
                    }

"""
import nltk
import opinion_classes as op


def get_reviews(fname):
    """
    returns: a list of reviews, which contain a list of sentences
    """
    file = open(fname)
    reviews = []
    for line in file:
        cols = line.split(',')
        r_id = int(cols[0])
        s_id = int(cols[1])
        text = cols[2].strip()
        sentences = []
        if r_id < len(reviews): #still the same review
            sentences = reviews[r_id]
        else:
            reviews.append(sentences)
        sentences.append(text)
    return reviews

def get_opinion_words(fname, orientation):
    """
    returns: a list of OpinionWords
    """
    #not going to worry about synonyms and antonyms yet
    file = open(fname)
    opwords = []
    for line in file:
        opwords.append(op.OpinionWord(line.replace("\n",""), orientation))
    return opwords

def get_features(fname):
    """
    returns: a dict of with keys (review_id, sent_id) and list of Features as values
    """
    file = open(fname)
    features = {}
    for line in file:
        cols = line.split(',')
        r_id = int(cols[0])
        s_id = int(cols[1])
        f = cols[2].strip()
        if (r_id,s_id) not in features:
            features[(r_id,s_id)] = [op.Feature(f)]
        else:
            features[(r_id,s_id)].append(op.Feature(f))
    return features

def get_pos(sentence):
    """
    returns: a list of (word, pos) pairs for each word in the sentence
    """
    return nltk.pos_tag(nltk.word_tokenize(sentence))

def parse_opinion_files(fnames):
    """
    fnames:  a dictionary of file names

    returns: the output as described above
    """
    reviews = get_reviews(fnames['reviews'])
    opwords = get_opinion_words(fnames['pos_opwords'], 1)
    opwords.extend(get_opinion_words(fnames['neg_opwords'], -1))
    features = get_features( fnames['features'])
    return combine(reviews, opwords, features)

def combine(reviews, opwords, features):
    """
    a helper for parse_opinion_files
    """
    reviews_list = []
    for r_id in range(0,len(reviews)):
        review_list = []
        for s_id in range(0,len(reviews[r_id])):
            sent = reviews[r_id][s_id]
            feature_dict = {}
            if (r_id,s_id) in features:
                for f in features[(r_id,s_id)]: 
                    feature_dict[f.name] = (f, 0)
            opword_dict = {}
            for opw in opwords:
                opw_name = ' ' + opw.name + ' ' #checks if the word is in the sentence
                if sent.partition(opw_name)[1] == opw_name and opw.name not in feature_dict:
                    opword_dict[opw.name] = (opw, 0)
            pos_sent = get_pos(sent)
            s_dict = {"id":s_id,"text":pos_sent,"features":feature_dict,"opinion_words":opword_dict}
            review_list.append(s_dict)
        reviews_list.append(review_list)
    return reviews_list
            
