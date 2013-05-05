#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn

def plot_roc(roc_file,style,label_str):
    x_vals = [] #FPR
    y_vals = [] #TPR
    for line in roc_file:
        tpr,fpr = line.split(',')
        x_vals.append(float(tpr))
        y_vals.append(float(fpr))
    plt.plot(x_vals,y_vals,style,label=label_str)


output = sys.argv[1]
title = sys.argv[2]
fig = plt.figure()
fig.suptitle(title,fontsize=14,fontweight='bold')

#opinions
file1 = open(sys.argv[3])
label1 = sys.argv[4]
plot_roc(file1,"r",label1)
file1.close()

#tf-idf
file2 = open(sys.argv[5])
label2 = sys.argv[6]
plot_roc(file2,"g",label2)
file2.close()

#filtered-tf-idf
file3 = open(sys.argv[7])
label3 = sys.argv[8]
plot_roc(file3,"b",label3)
file3.close()

plt.legend(loc='best')
plt.savefig(output, dpi=400, bbox_inches='tight')
