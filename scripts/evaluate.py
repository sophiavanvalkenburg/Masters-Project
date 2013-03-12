#!/usr/bin/python

"""
_________________ref________________
hyp |       | pos   | neg   |absent |
    |pos    |       |       |       |
    |       |       |       |       |
    |neu    |       |       |       |
    |       |       |       |       |
    |neg    |       |       |       |
    |       |       |       |       |
    |absent |       |       |       |
____|_______|_______|_______|_______|

"""


import sys
import nltk

"""
get_values: returns (hyps,refs) tuple with only specified (pos/neg/all) items selected
"""
def get_values(hyps, refs, vals):
    filtered_hyps = []
    filtered_refs = []
    for i in range(0,len(refs)):
        r = refs[i]
        h = hyps[i]
        r_op = int(r.split(',')[3])
        h_op = int(h.split(',')[3])
        if r_op in vals:
            filtered_refs.append(r)
        if h_op in vals:
            filtered_hyps.append(h)
        elif r_op in vals and h_op == 0:
            filtered_hyps.append(h)
    return (filtered_hyps, filtered_refs)

def fraction_incorrect(hyps, refs, test_val, vals):
    counter = 0
    total = 0
    for i in range(0,len(refs)):
        r = int(refs[i].split(',')[3])
        h = int(hyps[i].split(',')[3])
        if r in vals and h != r:
            if h == test_val:
                counter += 1
                total += 1
            else:
                total += 1
    return float(counter)/total

hyp_fname = sys.argv[2]     #the hypothesis file
ref_fname = sys.argv[3]   #the reference (truth) file
mode = sys.argv[1] #nothing or -t: total; -p: positive scores; -n: negative scores 

hyp_file = open(hyp_fname)
ref_file = open(ref_fname)

hyps = hyp_file.readlines()
refs = ref_file.readlines()

f_neutral = 0.0

if mode == '-p':
    print "Scores for positive opinions"
    f_neutral = fraction_incorrect(hyps, refs,0,[1])
    (hyps,refs) = get_values(hyps,refs,[1])
elif mode == '-n':
    print "Scores for negative opinions"
    f_neutral = fraction_incorrect(hyps,refs,0,[-1])
    (hyps,refs) = get_values(hyps,refs,[-1])
elif mode == '-t':
    print "Scores for all opinions"
    f_neutral = fraction_incorrect(hyps,refs,0,[1,-1])
    (hyps,refs) = get_values(hyps,refs,[1,-1])
else:
    print "usage: evaluate [mode] [hyp] [ref] where [mode] is '-p' (positive), '-n' (negative) or '-t' (total)"
    exit(1)

print "Total features:",len(refs)
print "Precision:",nltk.metrics.scores.precision(set(refs),set(hyps))
print "Recall:",nltk.metrics.scores.recall(set(refs),set(hyps))
print "F-Measure:",nltk.metrics.scores.f_measure(set(refs),set(hyps))
print "Fraction of Incorrect were Neutral:",f_neutral
print ""

"""
POS = 1
NEG = -1
NEU = 0
ABS = "abs"

def get_dict(file):
    d = {}
    for row in file:
        cols = row.split(',')
        r_id = int(cols[0]) #review id
        s_id = int(cols[1]) #sentence id
        if (r_id,s_id) not in d:
            d[(r_id,s_id)] = {}
        feature = cols[2].strip()
        orientation = int(cols[3])
        d[(r_id,s_id)][feature] = orientation
    return d

hyp_file = open(hyp_fname)
ref_file = open(ref_fname)

hyps = get_dict(hyp_file)
refs = get_dict(ref_file)
conf_m = {POS:{POS:0, NEG:0, ABS:0},NEU:{POS:0,NEG:0,ABS:0},NEG:{POS:0,NEG:0,ABS:0},ABS:{POS:0,NEG:0,ABS:0}} #confusion matrix

for s in hyps:
    sent = hyps[s]
    for feature in sent:
        orientation = sent[feature]
        if s not in refs or feature not in refs[s]:
            conf_m[orientation][ABS] += 1
        else:
        #    if orientation == 0: print s,feature
            ref_orientation = refs[s][feature]
            conf_m[orientation][ref_orientation] += 1
for s in refs:
    sent = refs[s]
    for feature in sent:
        orientation = sent[feature]
        if s not in hyps or feature not in hyps[s]:
            conf_m[ABS][orientation] += 1

print conf_m

print "Precision for POS:",conf_m[POS][POS]/float(conf_m[POS][POS]+conf_m[POS][NEG])
print "Precision for NEG:",conf_m[NEG][NEG]/float(conf_m[NEG][NEG]+conf_m[NEG][POS])
print "Recall for POS:",conf_m[POS][POS]/float(conf_m[POS][POS]+conf_m[NEU][POS]+conf_m[NEG][POS])
print "Recall for NEG:",conf_m[NEG][NEG]/float(conf_m[NEG][NEG]+conf_m[NEU][NEG]+conf_m[POS][NEG])
print "Overall Precision:",(conf_m[POS][POS]+conf_m[NEG][NEG])/float(conf_m[POS][POS]+conf_m[NEG][NEG]+conf_m[POS][NEG]+conf_m[NEG][POS])
print "Overall Recall:",(conf_m[POS][POS]+conf_m[NEG][NEG])/float(conf_m[POS][POS]+conf_m[NEG][NEG]+conf_m[NEU][POS]+conf_m[NEU][NEG]+conf_m[POS][NEG]+conf_m[NEG][POS])
"""
