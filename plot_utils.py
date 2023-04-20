import matplotlib.pyplot as plt
import logging as lg


def plot_list(_lst, _label):
    x = list(range(len(_lst)))
    plt.plot(x, _lst, label=_label)
    #plt.show()

def plot_load_shock(_lst):
    load = [_lst[0] for _ in range(_lst[1])]
    #load.append([_lst[0] for _ in range(_lst[1])])
    load.extend([_lst[0] * _lst[4] for _ in range(_lst[1], _lst[2])])
    load.extend([_lst[0] for _ in range(_lst[2], _lst[3])])
    x = list(range(_lst[3]))
    plt.plot(x, load)

def plot_trigger_and_measurement(_measurement, _trigger):
    plot_list(_measurement)
    plot_load_shock(_trigger)
    plt.show()

def plot_measurements(_syst, args):
    if args.plot_dropped:
        plot_list(_syst.dropped_reqs, "Dropped")
    if args.plot_served:
        plot_list(_syst.served_reqs, "Served")
    if args.plot_retried:
        plot_list(_syst.retried_reqs, "Retried")
    plt.legend()
    plt.show()