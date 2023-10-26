import matplotlib.pyplot as plt
import numpy as np
import argparse
import logging as lg

def plot_results(_avg_len):
    retried_withgc = []
    responded_withgc = []
    retried_nogc = []
    responded_nogc = []
    ratio_withgc = []
    ratio_nogc = []
    with open("../Experiment_results/exp2.txt", "r") as f:
        content = f.readlines()
        x = len(content)
        for i in range(x):
            line = content[i]
            if i >= x/2:
                vals = line.split()
                retried_withgc.append(float(vals[0]))
                responded_withgc.append(float(vals[1]))
                ratio_withgc.append(float(vals[2]))
            else:
                vals = line.split()
                retried_nogc.append(float(vals[0]))
                responded_nogc.append(float(vals[1]))
                ratio_nogc.append(float(vals[2]))
                
    
    plt.ylabel("ratio")
    plt.plot(ratio_withgc, 'r')
    plt.plot(ratio_nogc, 'g')
    plt.show()
    
    
if __name__ == "__main__":
    plot_results(0)