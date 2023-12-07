import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import argparse
import logging as lg

def process_results(default_start, default_end, spike_start, spike_end):
    with open("../Experiment_results/exp8_00.txt", "r") as f:
        content = f.readlines()
        count = 0
        len_x = default_end - default_start
        len_y = spike_end - spike_start
        len_rand = 20
        x_index = np.zeros((len_x, len_y))
        y_index = np.zeros((len_x, len_y))
        throughput_mode1 = np.zeros((len_x, len_y))
        total_efficiency = 0
        
        for i in range(3):
            for j in range(len_y):
                x_index[i][j] = i+default_start
                y_index[i][j] = j+spike_start
                avg_ratio = 0
                # total_req_num = (i+default_start)* (200-15) + (j+spike_start)*15
                for k in range(len_rand):
                    line = content[count]
                    vals = line.split()
                    # retried_withgc.append(float(vals[0]))
                    # responded_withgc.append(float(vals[1]))
                    avg_ratio += float(vals[4]) / float(vals[3])
                    count += 1
                throughput_mode1[i][j] = avg_ratio /len_rand
                total_efficiency += avg_ratio /len_rand
    
    total_efficiency = total_efficiency / (3 * len_y)
    print(total_efficiency)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax.set_zlabel('effiency')
    ax.set_xlabel('default')
    ax.set_ylabel('spike')
    
    
    ax.plot_surface(x_index, y_index, throughput_mode1,cmap = cm.Blues, linewidth=0, antialiased=False)
    # ax.plot_surface(x_index, y_index, ratio_withgc, linewidth=0, antialiased=False)
    plt.savefig("efficiency_02")
    
    plt.show()
    
    
if __name__ == "__main__":
    process_results(6,13,6,20)