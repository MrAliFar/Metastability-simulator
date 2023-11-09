import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import argparse
import logging as lg

def plot_results( spike_start, spike_end):
    retried_withgc = []
    responded_withgc = []
    retried_nogc = []
    responded_nogc = []

    with open("../Experiment_results/exp4.txt", "r") as f:
        content = f.readlines()
        count = 0
        len_y = spike_end - spike_start
        len_rand = 20
        y_index = np.zeros( len_y*len_rand)
        ratio_withcontrol = np.zeros(len_y*len_rand)
        ratio_nocontrol = np.zeros(len_y*len_rand)
        avg_green = np.zeros(len_y)
        avg_red = np.zeros(len_y)
        y = np.zeros(len_y)
        
        for j in range(len_y):
            avg = 0
            y[j] = j
            for k in range(len_rand):
                y_index[j*len_rand + k] = j+spike_start + float(k)/len_rand
                line = content[count]
                vals = line.split()
                # retried_withgc.append(float(vals[0]))
                # responded_withgc.append(float(vals[1]))
                count += 1
                ratio_withcontrol[j*len_rand + k] = float(vals[2])
                avg += float(vals[2])
            avg = avg/10
            avg_red[j] = avg
            
                    
        for j in range(len_y):
            avg = 0
            for k in range(len_rand):
                y_index[j*len_rand + k] = j+spike_start + float(k)/len_rand
                line = content[count]
                vals = line.split()
                # retried_withgc.append(float(vals[0]))
                # responded_withgc.append(float(vals[1]))
                count += 1
                ratio_nocontrol[j*len_rand + k] = float(vals[2])
                avg += float(vals[2])
            avg = avg/10
            avg_green[j] = avg
    
    fig, ax = plt.subplots()
    ax.set(xlabel='spikeload', ylabel='ratio',title='mode_0_2_update')
    ax.grid()
    
    fig1, ax1 = plt.subplots()
    
    ax.plot( y_index, ratio_nocontrol, 'g')
    ax.plot( y_index, ratio_withcontrol, 'r')
    ax1.plot( y , avg_green, 'g')
    ax1.plot( y, avg_red, 'r')
    plt.axhline(y=np.nanmean(ratio_nocontrol), color='g')
    plt.axhline(y=np.nanmean(ratio_withcontrol), color='r')
    
    plt.show()
    
    
    
if __name__ == "__main__":
    plot_results(6,21)