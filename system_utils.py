from queue import Queue
import logging as lg

import template_utils

class system:
    def __init__(self):
        self.services = []
    
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
            agt_id += 1


class service:
    def __init__(self, _id):
        self.id = _id
        self.agents = []

class agent:
    def __init__(self, _id, _in_queue_cap, _out_queue_cap, _pending_queue_cap, _srvc_rate, _send_rate, _timeout, _backoff_behavior):
        self.id = _id
        self.in_queue = Queue(_in_queue_cap)
        self.out_queue = Queue(_out_queue_cap)
        self.pending_queue = Queue(_pending_queue_cap)
        self.srvc_rate = _srvc_rate
        self.send_rate = _send_rate
        self.timeout = _timeout
        self.backoff_behavior = _backoff_behavior
        #### The map taking account of whether a serve event has been added to the agent's
        #### events at a particular time slot.
        self.serve_events = dict()
        #### The map taking account of whether a send event has been added to the agent's
        #### events at a particular time slot.
        self.send_events = dict()

def generate_system():
    """
    The interface provided by the package to other packages that need to create a system.
    """
    syst = system()
    syst.create_topology()
    syst.set_services()
    return syst