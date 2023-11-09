import numpy as np
import logging as lg
from queue import Queue
import argparse

import client_utils
import event_utils
import system_utils
import failure_utils
import template_utils
import measurement_utils
import debug_utils
import plot_utils
import backoff_utils
import monitor_utils

def start_sim(args: argparse.Namespace):
#def start_sim(_network_delay, _sim_len, _num_reqs):
    #### This is the main event data structure: index i is the priority queue
    #### for the events of time slot i.
    #### Initiate the system
    syst = system_utils.generate_system(args.sim_len)
    events = syst.events
    if args.load == "LOAD_SHOCK_STATIC":
        # print("make system non random")
        syst.random = False
    for _service in syst.services:
        for _agent in _service.agents:
            # print(args.garbage_collect)
            # print(args.garbage_collect == 1)
            _agent.garbage_collect = (args.garbage_collect == 1)
    if args.controller is not None:
        syst.monitor.active = (args.controller != -1)
        syst.monitor.active_control = args.controller
        
    #### Generate the client requests
    reqs = client_utils.issue_client_requests(args.input_duration, args.num_reqs, args.load)
    debug_utils.print_unwrapped(reqs)
    #### Enter the client requests into the event priority queue.
    event_utils.issue_client_events(events, reqs)
    event_utils.issue_measurement_events(events)
    #### Get the failures from the config, and add them as events.
    if args.issue_failures:
        lg.info(f"Hi!{args.issue_failures}")
        failures = failure_utils.get_failures()
        event_utils.issue_failure_events(events, failures)
    #### Get the mitigations from the config, and add them as events.
    if args.issue_mitigations:
        mitigations = failure_utils.get_mitigations()
        event_utils.issue_mitigation_events(events, mitigations)
    #### Initiate monitor check
    # syst.monitor.start_new_round(syst, 3)
    #### Start the simulation
    for i in range(args.sim_len):
        #lg.info(f"time is {i}")
        
        #debug_utils.print_list_unwrapped(events[i])
        syst.time = i
        # refresh timeoutchange for every agent here
        backoff_utils.timeout_change_newtimeslot(syst)
        if (args.monitor_policy == "HEART_BEAT"):
            if(i % args.monitor_frequency == 0):
                syst.monitor.start_new_heartbeat_round(syst, i)
        if (args.monitor_policy == "PING"):
            if(i % args.monitor_frequency == 0):
                syst.monitor.start_new_ping_round(syst, i)
        # print("finish")
        ####handle events starting from timeslot 1
        if len(events[i]) == 0:
            continue
        else:
            while not len(events[i]) == 0:
                evs = event_utils.handle_event(events[i][0], syst, i, args.network_delay, args.sim_len)
                #lg.debug("New event")
                #print(f"ev is {ev}")
                event_utils.deleteNode(events[i], events[i][0])
                if not evs == -1:
                    for ev in evs:
                        if not ev == -1:
                            event_utils.insert(events[ev.time], ev)
                            #debug_utils.print_unwrapped([ev])
    trigger = template_utils.parse_trigger()[0]
    
    #plot_utils.plot_trigger_and_measurement(syst.dropped_reqs, trigger)
    plot_utils.plot_measurements(syst, args)
    
    #plot_utils.plot_list(syst.dropped_reqs)
    if args.issue_failures:
        lg.warning("Logging metastability!")
        slope_responded, slope_retried = measurement_utils.is_metastable(syst, failures[0].time)
    else:
        slope_responded, slope_retried = measurement_utils.is_metastable(syst, 1)
    if args.exp_no > 0:
        file_name = "./Experiment_results/exp"+str(args.exp_no)+".txt"
        newstring = str(slope_retried) + " " + str(slope_responded) + " "
        if not slope_responded == 0:
            newstring +=  str(slope_retried / slope_responded) 
        else:
            newstring +=  str(-1) 
        newstring += " " + str(len(reqs))+ " " + str(syst.responded_reqs[len(syst.responded_reqs) - 1]) + " " + str(syst.retried_reqs[len(syst.retried_reqs) - 1])
        newstring += "\n"
        template_utils.write_to_file(file_name, newstring)
        

if __name__ == "__main__":
    #lg.basicConfig(format = "%(asctime)s %(filename)s:%(lineno)d %(message)s",level = lg.DEBUG)
    ##### To clear the contents of the file:
    log_file = open("log.txt", 'w')
    # log_file.close()
    lg.basicConfig(filename="log.txt", format = "%(filename)s:%(lineno)d %(message)s", level = lg.DEBUG)
    
    #### Parse arguments:
    ########## 1. Simulation length
    ########## 2. Number of services
    ########## 3. System topology
    ########## 4. Number of agents for each service
    ########## 5. The spec for each agent
    parser = argparse.ArgumentParser()
    parser.add_argument_group('General')
    parser.add_argument('--exp_no',
                        type=int,
                        required=True,
                        help='The number of the experiment to run. Zero indicates manual runs.')
    parser.add_argument('--input_duration',
                        type=int,
                        required=True,
                        help='The duration of imposing the system to input.')
    parser.add_argument('--sim_len',
                        type=int,
                        required=True,
                        help='The length of the simulation. It allows things to cool off after the input phase.')
    parser.add_argument('--num_reqs',
                        type=int,
                        required=True,
                        help='The number of requests.')
    parser.add_argument('--network_delay',
                        type=int,
                        required=True,
                        help='Network delay. Fixed for all p2p communication.')
    parser.add_argument('--load',
                        type=str,
                        required=True,
                        choices=['AUTO', 'LOAD_SHOCK', 'EMPTY', 'LOAD_SHOCK_STATIC'],
                        help='The type of the load, e.g., automatic, load shock, etc.')
    parser.add_argument_group('Failure-Flags')
    parser.add_argument('--issue_failures',
                        type=int,
                        required=True,
                        help='Whether to issue the failure events or not.')
    parser.add_argument('--issue_mitigations',
                        type=int,
                        required=True,
                        help='Whether to issue the mitagation events or not.')
    parser.add_argument_group('Plot-Flags')
    parser.add_argument('--plot_dropped',
                        type=int,
                        required=True,
                        help='Whether to plot the cumulative dropped requests in the entire system.')
    parser.add_argument('--plot_receive_dropped',
                        type=int,
                        required=True,
                        help='Whether to plot the cumulative receive-dropped requests in the entire system.')
    parser.add_argument('--plot_pending_dropped',
                        type=int,
                        required=True,
                        help='Whether to plot the cumulative pending-dropped requests in the entire system.')
    parser.add_argument('--plot_served',
                        type=int,
                        required=True,
                        help='Whether to plot the cumulative served requests in the entire system.')
    parser.add_argument('--plot_responded',
                        type=int,
                        required=True,
                        help='Whether to plot the cumulative responded requests in the entire system.')
    parser.add_argument('--plot_retried',
                        type=int,
                        required=True,
                        help='Whether to plot the cumulative retried requests in the entire system.')
    parser.add_argument('--plot_failures',
                        type=int,
                        required=True,
                        help='Whether to plot the failure boundaries.')
    parser.add_argument('--plot_mitigations',
                        type=int,
                        required=True,
                        help='Whether to plot the mitigation boundaries.')
    parser.add_argument('--plot_service_dropped',
                        type=int,
                        required=True,
                        help='Whether to plot the dropped requests for each service.')
    parser.add_argument('--plot_enabled',
                        type=int,
                        required=True,
                        help="A general flag to enable or disable plots.")
    parser.add_argument('--monitor_policy',
                        type=str,
                        required=True,
                        choices=['PING', 'HEART_BEAT','NONE'],
                        help="Which policy monitor should operate on.")
    parser.add_argument('--monitor_frequency',
                        type=int,
                        required=True,
                        help="How often monitor takes action.")
    parser.add_argument('--garbage_collect',
                        type= int,
                        required=True,
                        help="Whether agents need to perform garbage collect.")
    parser.add_argument('--controller',
                        type= int,
                        required=False,
                        help="controller function is on if input == 1 ")

    args = parser.parse_args()
    #network_delay = 1
    #sim_len = 100
    #num_reqs = 50
    
    #start_sim(network_delay, sim_len, num_reqs)
    start_sim(args)