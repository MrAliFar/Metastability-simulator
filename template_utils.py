import logging as lg

def parse_communication_patterns():
    """
    Parse the request template file to extract the allowable communication patterns.
    
    Example: 1-2-1
    
    Output:
        - A list of allowable patterns. Each pattern is a list itself.
    """
    
    patterns = []
    acks = []
    with open('./Configs/communication_patterns.txt', 'r') as f:
        for line in f:
            splitted = line.split(":")
            pat = splitted[1].split("-")
            for i in range(len(pat)):
                pat[i] = int(pat[i])
            if not verify_communication_pattern(pat):
                lg.error('Invalid request template')
                #### TODO: handle this error return.
                return []
            patterns.append(pat)
            ack = splitted[2].split("-")
            for i in range(len(ack)):
                ack[i] = int(ack[i])
            acks.append(ack)
    return patterns, acks

#### TODO:
def create_communication_patterns():
    """
    A helper function to systematically create the request template file.
    """
    pass

#### TODO:
def verify_communication_pattern(_pattern):
    """
    A helper function to verify whether a given communication pattern is allowed
    in the system topology.
    """
    return True

def parse_system_adjacency_matrix():
    """
    Parse the system adjacency matrix file to extract the system topology.
    
    Example: 1 1\n 1 1
    
    Output:
        - The adjacency matrix associated to the system's topology
    """
    mat = []
    with open('./Configs/system_topology.txt', 'r') as f:
        for line in f:
            mat.append([])
            vals = line.split()
            for i in range(len(vals)):
                vals[i] = int(vals[i])
            mat[len(mat) - 1] = vals
    
    return mat

def parse_agent_config():
    """
    Parse the agent configs file to extract the configuration for each agent.
    
    Example: 1:ADD:5:5:2:2:3. Here, 1 refers to the service the agent belongs to, and ADD
    specifies that the agent's backoff behavior is additive. There are two general
    backoff types for now:
        + ADD
        + MUL
    The rest designate in_queue_cap, out_queue_cap, pending_queue_cap, srvc_rate, and
    the initial timeout value.
    
    Output:
        - The list of agent configs. Each config is a list itself.
    """
    
    agent_configs = []
    with open('./Configs/agents_config.txt', 'r') as f:
        for line in f:
            vals = line.split(":")
            for i in range(len(vals)):
                if i == len(vals) - 1:
                    vals[i] = vals[i].split()[0]
                else:
                    vals[i] = int(vals[i])
            agent_configs.append(vals)
    
    return agent_configs
