import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import logging as lg
import matplotlib.ticker as plticker

def plot_results(default_start, default_end, spike_start, spike_end):
    with open("../Experiment_results/exp10_tail_lat_throughput.txt", "r") as f:
        content = f.readlines()
        count = 0
        len_x = default_end - default_start
        len_y = spike_end - spike_start
        len_rand = 20
        x_index = np.zeros((len_x, len_y))
        y_index = np.zeros((len_x, len_y))
        throughput_mode1 = np.zeros((len_x, len_y))
        throughput_mode2 = np.zeros((len_x, len_y))
        len_agents = 12
        
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
                    avg_ratio += float(vals[5])/float(vals[3])
                    count += 1
                throughput_mode1[i][j] = avg_ratio / len_rand

    with open("../Experiment_results/exp10_tail_latency.txt", "r") as f:
        content = f.readlines()
        count = 0
        for i in range(default_end - default_start):
            for j in range(spike_end - spike_start):
                x_index[i][j] = i+default_start
                y_index[i][j] = j+spike_start
                avg_latency = 0
                for k in range(len_rand*len_agents):
                    line = content[count]
                    count += 1
                    line =  line.split( sep= '|')
                    x_vals = line[0]
                    y_vals = line[1]
                    if len(y_vals) > 4:
                        y_vals = y_vals.split(',')[1:-2]
                    # print(y_vals)
                        y_vals = [eval(i) for i in y_vals]
                    # # retried_withgc.append(float(vals[0]))
                    # # responded_withgc.append(float(vals[1]))
                        avg_latency += sum(y_vals) / len(vals)
                throughput_mode2[i][j] = avg_latency / (len_rand *len_agents)
    
    
    fig, (ax1, ax2) = plt.subplots(1, 2,subplot_kw={"projection": "3d"})
    loc = plticker.MultipleLocator(base=1.0)
    ax1.xaxis.set_major_locator(loc)
    ax1.yaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)
    ax2.yaxis.set_major_locator(loc)
    ax1.set_zlabel('throughput')
    ax1.set_xlabel('default')
    ax1.set_ylabel('spike')
    ax1.plot_surface(x_index, y_index, throughput_mode1,cmap = cm.Blues, linewidth=0, antialiased=False)
    
    ax2.set_zlabel('tailatency')
    ax2.set_xlabel('default')
    ax2.set_ylabel('spike')
    ax2.plot_surface(x_index, y_index, throughput_mode2,cmap = cm.Blues, linewidth=0, antialiased=False)
    
    # ax.plot_surface(x_index, y_index, ratio_withgc, linewidth=0, antialiased=False)
    plt.savefig("ratio and tail latency")
    
    plt.show()
    
    
if __name__ == "__main__":
    plot_results(6,13,6,19)