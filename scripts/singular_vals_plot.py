#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn

def plot_sv(sv_file,style,label_str):
    count = 1
    x_vals = [] #line number
    y_vals = [] #singular values
    for line in sv_file:
        x_vals.append(count)
        y_vals.append(float(line))
        count+=1
    plt.plot(x_vals,y_vals,style,label=label_str)


output = sys.argv[1]
title = sys.argv[2]
fig = plt.figure()
fig.suptitle(title,fontsize=14,fontweight='bold')

sv_file1 = open(sys.argv[3])
label1 = sys.argv[4]
plot_sv(sv_file1,"r",label1)
sv_file1.close()

sv_file2 = open(sys.argv[5])
label2 = sys.argv[6]
plot_sv(sv_file2,"g",label2)
sv_file2.close()

sv_file3 = open(sys.argv[7])
label3 = sys.argv[8]
plot_sv(sv_file3,"b",label3)
sv_file3.close()

plt.legend(loc='best')
plt.savefig(output, dpi=400, bbox_inches='tight')
