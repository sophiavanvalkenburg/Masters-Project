#!/bin/python

class Feature:
    """
    A class that represents a feature of a product.

    The feature itself is represented by a string (name)
   
    The global orientation is implemented as a dictionary
    of (opinion word, orientation) pairs. It will also contain
    a '_default' key whose value is an orientation if the feature
    is an adjective, and None otherwise.
    """
    def __init__(self, name):
        self.name = name
        self.global_orientation = {}
        #set default to 0 initially; will change if it's adj
        self.global_orientation['_default'] = 0

class OpinionWord:
    """
    A class that represents an opinion word.
    
    The word itself is represented by a string (name)
    and includes two synonym and antonym lists (also OpinionWords)
    """
    def __init__(self, name, orientation,synonyms=[], antonyms=[]):
        self.name = name
        self.orientation = orientation
        self.synonyms = synonyms
        self.antonyms = antonyms
