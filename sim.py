import numpy as np
import logging as lg
from queue import Queue

import client_utils
import event_utils
import system_utils
import debug_utils


def start_sim(_sim_len, _num_reqs):
    #### This is the main event data structure: index i is the priority queue
    #### for the events of time slot i.
    events = []
    for _ in range(_sim_len):
        events.append([])
    #### Initiate the system
    syst = system_utils.generate_system()
    #### Generate the client requests
    reqs = client_utils.issue_client_requests(_sim_len, _num_reqs, "AUTO")
    debug_utils.print_unwrapped(reqs)
    #### Enter the client requests into the event priority queue.
    event_utils.issue_client_events(events, reqs)
    #### Start the simulation
    for i in range(_sim_len):
        debug_utils.print_list_unwrapped(events[i])
        lg.info(f"time is {i}")
        if len(events[i]) == 0:
            continue
        else:
            while not len(events[i]) == 0:
                ev = event_utils.handle_event(events[i][0], syst, i, _sim_len)
                lg.debug("New event")
                debug_utils.print_unwrapped([ev])
                #print(f"ev is {ev}")
                event_utils.deleteNode(events[i], events[i][0])
                if not ev == -1:
                    event_utils.insert(events[ev.time], ev)

if __name__ == "__main__":
    #lg.basicConfig(format = "%(asctime)s %(filename)s:%(lineno)d %(message)s",level = lg.DEBUG)
    lg.basicConfig(format = "%(filename)s:%(lineno)d %(message)s", level = lg.DEBUG)
    
    #### Parse arguments:
    ########## 1. Simulation length
    ########## 2. Number of services
    ########## 3. System topology
    ########## 4. Number of agents for each service
    ########## 5. The spec for each agent
    start_sim(10, 5)
