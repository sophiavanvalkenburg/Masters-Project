#!/usr/bin/python

import sys

def first_last_r_id(data):
    r_start = data[0]
    r_end = data[len(data)-1]
    cols_start = r_start.split(',')
    cols_end = r_end.split(',')
    return (int(cols_start[0]), int(cols_end[0]))

fname1 = sys.argv[1]
list1 = sys.argv[2]
fname2 = sys.argv[3]
list2 = sys.argv[4]

file1 = open(fname1)
file2 = open(fname2)
lines1 = file1.readlines()
lines2 = file2.readlines()
(start1, end1) = list1.split(":")
(start2, end2) = list2.split(":")
(start_id1, end_id1) = first_last_r_id(lines1)
(start_id2, end_id2) = first_last_r_id(lines2)
start1 = int(start_id1) if start1 == '' else int(start1)
end1 = int(end_id1)+1 if end1 == '' else int(end1)
start2 = int(start_id2) if start2 == '' else int(start2)
end2 = int(end_id2)+1 if end2 == '' else int(end2)

curr_id = -1
for l in lines1:
    cols = l.split(',')
    r_id = int(cols[0])
    if r_id != curr_id:
        curr_id = r_id
    if curr_id < start1: continue
    elif curr_id >= end1: break
    else: print l.strip(), ',', 0 #0 for normal review

next_id = curr_id+1

curr_id = -1
for l in lines2:
    cols = l.split(',')
    r_id = int(cols[0])
    if r_id != curr_id:
        curr_id = r_id
    if curr_id < start2: continue
    elif curr_id >= end2: break
    else: 
        print next_id+curr_id,
        for c in cols[1:]:
            print ',',c.strip(),
        print ',',1 #1 for anomalous review
