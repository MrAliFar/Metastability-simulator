import matplotlib.pyplot as plt
import logging as lg

import template_utils


def plot_list(_lst, _label, _marker):
    x = list(range(len(_lst)))
    plt.plot(x, _lst, label=_label, marker=_marker, markersize=2)
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
        plot_list(_syst.dropped_reqs, "Dropped", "o")
    if args.plot_receive_dropped:
        plot_list(_syst.receive_dropped_reqs, "Receive-dropped", "s")
    if args.plot_pending_dropped:
        plot_list(_syst.pending_dropped_reqs, "Pending-dropped", "x")
    if args.plot_served:
        plot_list(_syst.served_reqs, "Served", "D")
    if args.plot_retried:
        plot_list(_syst.retried_reqs, "Retried", "^")
    if args.issue_failures:
        failures = template_utils.parse_failures()
        plt.axvline(x=failures[0][2], color="r")
    if args.issue_failures:
        mitigations = template_utils.parse_mitigations()
        plt.axvline(x=mitigations[0][2], color="g")
    plt.legend()
    plt.show()