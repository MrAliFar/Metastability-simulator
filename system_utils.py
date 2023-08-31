from queue import Queue
import logging as lg

import template_utils
import monitor_utils

class system:
    def __init__(self):
        self.services = []
        self.receive_dropped_reqs = []
        self.pending_dropped_reqs = []
        self.dropped_reqs = []
        self.served_reqs = []
        self.served_client_reqs = []
        #### The number of requests that are responded to by the system.
        self.responded_reqs = []
        #### A dictionary taking account of the ids of the responded requests.
        self.responded_reqs_ids = dict()
        self.retried_reqs = []
        self.monitor = None
        self.monitor_address = [0,0]
        self.events = []

    
    def create_topology(self):
        """
        Uses the parsed adjacency matrix to create services.
        """
        self.topology = template_utils.parse_system_adjacency_matrix()
        for i in range(len(self.topology)):
            self.services.append(service(i))
    
    def set_services(self):
        """
        Populates the services with their corresponding agents. The agents are
        extracted from the corresponding config file.
        """
        agent_configs = template_utils.parse_agent_config()
        agt_id = 0
        for agt in agent_configs:
            self.services[agt[0]].agents.append(agent(agt_id, agt[1], agt[2], agt[3], agt[4], agt[5], agt[6], agt[7]))
            lg.info(f"The in cap for the agent is {self.services[agt[0]].agents[len(self.services[agt[0]].agents) - 1].in_queue.maxsize}")
            agt_id += 1


class service:
    def __init__(self, _id):
        self.id = _id
        self.agents = []
        self.receive_dropped_reqs = 0
        self.pending_dropped_reqs = 0
        self.dropped_reqs = 0
        #### The number of dropped requests based on time
        self.temporal_receive_dropped_reqs = []
        self.temporal_pending_dropped_reqs = []
        self.temporal_dropped_reqs = []
        self.served_reqs = 0
        self.served_client_reqs = 0
        self.retried_reqs = 0
        self.responded_reqs = 0
        self.dropped_monitor_reqs = 0

class agent:
    def __init__(self, _id, _in_queue_cap, _out_queue_cap, _pending_bag_cap, _srvc_rate, _send_rate, _timeout, _backoff_behavior):
        self.id = _id
        self.in_queue = Queue(_in_queue_cap)
        self.out_queue = Queue(_out_queue_cap)
        self.pending_bag = []
        self.pending_bag_cap = _pending_bag_cap
        self.srvc_rate = _srvc_rate
        self.original_srvc_rate = _srvc_rate
        #### The amount of service remaining at the moment. Resets to srvc_rate
        #### at each time slot.
        self.remaining_srvc = _srvc_rate
        self.send_rate = _send_rate
        self.timeout = _timeout ####initial timeout value
        self.backoff_behavior = _backoff_behavior
        self.timeout_index_cntr = 0
        self.timeout_bucket = 10 #### a token bucket for if there is any available retry
        #### The number of requests that the agent drops cumulatively
        self.receive_dropped_reqs = 0
        self.pending_dropped_reqs = 0
        self.dropped_reqs = 0
        #### The number of dropped requests based on time
        self.temporal_receive_dropped_reqs = []
        self.temporal_pending_dropped_reqs = []
        self.temporal_dropped_reqs = []
        #### The number of requests that the agent serves cumulatively
        self.served_reqs = 0
        #### The number of end-to-end client requests that the agent serves cumulatively
        self.served_client_reqs = 0
        #### The number of requests that the agent retries cumulatively
        self.retried_reqs = 0
        #### The number of requests that are finally responded to by the agent.
        self.responded_reqs = 0
        #### The map taking account of whether a serve event has been added to the agent's
        #### events at a particular time slot.
        self.serve_events = dict()
        #### The map taking account of whether a send event has been added to the agent's
        #### events at a particular time slot.
        self.send_events = dict()
        self.acked_reqs = dict()

def generate_system(_len):
    """
    The interface provided by the package to other packages that need to create a system.
    """
    syst = system()
    syst.create_topology()
    syst.set_services()
    syst.monitor = monitor_utils.monitor(syst.services)
    for _ in range(_len):
        syst.events.append([])
    return syst