import matplotlib.pyplot as plt
import numpy as np
import argparse
import logging as lg

def plot_results(_avg_len):
    ratios = []
    with open("../Experiment_results/exp1.txt", "r") as f:
        for line in f:
            if not line == "\n":
                vals = line.split()
                ratios.append(float(vals[-1]))

    max_ratio = np.max(ratios)
    for i in range(len(ratios)):
        if ratios[i] == -1:
            ratios[i] = 2 * max_ratio
    
    avg_ratios = []
    num = int(len(ratios) / _avg_len)
    for i in range(num):
        sum = np.sum(ratios[i * _avg_len : (i + 1) * _avg_len])
        avg_ratios.append(sum / _avg_len)

    plt.plot(avg_ratios)
    #plt.axhline(y=max_ratio, color='r')
    plt.show()

def plot_results_2d(_avg_len):
    retried = []
    responded = []
    with open("../Experiment_results/exp1.txt", "r") as f:
        for line in f:
            if not line == "\n":
                vals = line.split()
                retried.append(float(vals[0]))
                responded.append(float(vals[1]))
    
    avg_retried = []
    avg_responded = []
    num = int(len(retried) / _avg_len)
    for i in range(num):
        sum_ret = np.sum(retried[i * _avg_len : (i + 1) * _avg_len])
        avg_retried.append(sum_ret / _avg_len)
        sum_res = np.sum(responded[i * _avg_len : (i + 1) * _avg_len])
        avg_responded.append(sum_res / _avg_len)
    plt.scatter(avg_responded, avg_retried)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--avg_len',
                        type=int,
                        required=True,
                        help='The number of samples for each num_requests value.')
    args = parser.parse_args()
    #plot_results(args.avg_len)
    plot_results_2d(args.avg_len)

