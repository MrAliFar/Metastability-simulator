import matplotlib.pyplot as plt
import logging as lg

import template_utils


def plot_list(_lst, _label, _marker):
    x = list(range(len(_lst)))
    plt.plot(x, _lst, label=_label, marker=_marker, markersize=2)
    #plt.show()
    
def plot_x_y(x, y, name):
    plt.plot(x,y,label = name, color="b")

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

def plot_tail_latency(_syst):
    plt.subplot(122)
    
    for _ in range(1,len(_syst.services)):
        _serv = _syst.services[_]
        for _agt in _serv.agents:
            plt.ylabel("tail_latency")
            plt.xlabel("time")
            plt.plot(_agt.tail_latency_x_list, _agt.tail_latency_list)
            # print(_agt.tail_latency_x_list)
            print(_agt.tail_latency_list)
            # new_x += _agt.tail_latency_x_list
            # new_y += _agt.tail_latency_list

def plot_measurements(_syst, args):
    plt.figure()
    plt.subplot(121)
    if args.plot_enabled:
        if args.plot_dropped:
            plot_list(_syst.dropped_reqs, "Dropped", "o")
        if args.plot_receive_dropped:
            plot_list(_syst.receive_dropped_reqs, "Receive-dropped", "s")
        if args.plot_pending_dropped:
            plot_list(_syst.pending_dropped_reqs, "Pending-dropped", "x")
        if args.plot_served:
            plot_list(_syst.served_reqs, "Served", "D")
        if args.plot_responded:
            plot_list(_syst.responded_reqs, "Responded", "D")
        if args.plot_retried:
            plot_list(_syst.retried_reqs, "Retried", "^")
        if args.plot_service_dropped:
            for i in range(len(_syst.services)):
                plot_list(_syst.services[i].temporal_dropped_reqs, "Service-dropped "+str(i), "D")
                plot_list(_syst.services[i].temporal_receive_dropped_reqs, "Service-receive-dropped "+str(i), "D")
                plot_list(_syst.services[i].temporal_pending_dropped_reqs, "Service-pending-dropped "+str(i), "D")
        if args.issue_failures and args.plot_failures:
            failures = template_utils.parse_failures()
            plt.axvline(x=failures[0][2], color="r")
        if args.issue_failures and args.plot_failures:
            mitigations = template_utils.parse_mitigations()
            plt.axvline(x=mitigations[0][2], color="g")
        # plot_list(_syst.served_monitor_reqs, "Monitor", "D")
        if args.plot_tail_latency is not None:
            if args.plot_tail_latency == 1:
                plot_tail_latency(_syst)

        # plot_x_y(new_x, new_y, "tail_latency")
        plt.legend()
        plt.savefig("result_for_current_run")
        plt.show()