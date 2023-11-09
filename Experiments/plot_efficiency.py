import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import argparse
import logging as lg

def plot_results(default_start, default_end, spike_start, spike_end):
    retried_withgc = []
    responded_withgc = []
    retried_nogc = []
    responded_nogc = []
    ratio_withgc = []
    ratio_nogc = []
    with open("../Experiment_results/exponential_1_2.txt", "r") as f:
        content = f.readlines()
        count = 0
        len_x = default_end - default_start
        len_y = spike_end - spike_start
        len_rand = 20
        x_index = np.zeros((len_x, len_y))
        y_index = np.zeros((len_x, len_y))
        ratio_withgc = np.zeros((len_x, len_y))
        ratio_nogc = np.zeros((len_x, len_y))
        
        for i in range(len_x):
            for j in range(len_y):
                x_index[i][j] = i+default_start
                y_index[i][j] = j+spike_start
                avg_ratio = 0
                for k in range(len_rand):
                    line = content[count]
                    vals = line.split()
                    # retried_withgc.append(float(vals[0]))
                    # responded_withgc.append(float(vals[1]))
                    avg_ratio += float(vals[4])/float(vals[3])
                    count += 1
                ratio_withgc[i][j] = avg_ratio
                    
        for i in range(default_end - default_start):
            for j in range(spike_end - spike_start):
                x_index[i][j] = i+default_start
                y_index[i][j] = j+spike_start
                avg_ratio = 0
                for k in range(len_rand):
                    line = content[count]
                    vals = line.split()
                    # retried_withgc.append(float(vals[0]))
                    # responded_withgc.append(float(vals[1]))
                    avg_ratio += float(vals[4])/float(vals[3])
                    count += 1
                ratio_nogc[i][j] = avg_ratio
    
    ratio_dif = (ratio_nogc - ratio_withgc)/ len_rand
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax.set_zlabel('efficiency')
    ax.set_xlabel('default')
    ax.set_ylabel('spike')
    
    
    ax.plot_surface(x_index, y_index, ratio_dif,cmap = cm.Blues, linewidth=0, antialiased=False)
    # ax.plot_surface(x_index, y_index, ratio_withgc, linewidth=0, antialiased=False)
    plt.savefig("efficiency")
    
    plt.show()
    
    
if __name__ == "__main__":
    plot_results(2,11,2,17)