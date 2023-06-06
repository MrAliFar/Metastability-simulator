import template_utils
import request_utils
from random import randint

def issue_client_requests(sim_len, num_reqs, _policy):
    """
    A function that creates the initial client requests.
    
    Input:
        - sim_len: The length of the simulation.
        - num_reqs: The number of the requests to be generated.
    Output:
        - A list of requests.
    """
    #### Parse the request templates.
    req_patterns, req_acks = template_utils.parse_communication_patterns()
    syst_id_cntr = 0
    if _policy == "AUTO":
        #### Issue requests selected uniformly at random from the parsed
        #### requests. The requests differ based on their communication pattern.
        reqs = []
        for _ in range(num_reqs):
            ts = randint(0, sim_len - 1)
            pattern_index = randint(0, len(req_patterns) - 1)
            reqs.append(request_utils.create_request(request_utils.EXTERNAL, req_patterns[pattern_index], req_acks[pattern_index], -1, ts, syst_id_cntr))
            syst_id_cntr += 1
    else:
        #### Manual generation of requests. This will be handy when studying the effect
        #### of load-increasing events.
        reqs = generate_requests(_policy)

    return reqs

def generate_requests(_policy):
    req_patterns, req_acks = template_utils.parse_communication_patterns()
    reqs = []
    syst_id_cntr = 0
    if _policy == "LOAD_SHOCK":
        trigger = template_utils.parse_trigger()[0]
        for ts in range(trigger[1]):
            for _ in range(trigger[0]):
                pattern_index = randint(0, len(req_patterns) - 1)
                reqs.append(request_utils.create_request(request_utils.EXTERNAL, req_patterns[pattern_index], req_acks[pattern_index], -1, ts, syst_id_cntr))
                syst_id_cntr += 1
        for ts in range(trigger[1], trigger[2]):
            for _ in range(trigger[0] * trigger[4]):
                pattern_index = randint(0, len(req_patterns) - 1)
                reqs.append(request_utils.create_request(request_utils.EXTERNAL, req_patterns[pattern_index], req_acks[pattern_index], -1, ts, syst_id_cntr))
                syst_id_cntr += 1
        for ts in range(trigger[2], trigger[3]):
            for _ in range(trigger[0]):
                pattern_index = randint(0, len(req_patterns) - 1)
                reqs.append(request_utils.create_request(request_utils.EXTERNAL, req_patterns[pattern_index], req_acks[pattern_index], -1, ts, syst_id_cntr))
                syst_id_cntr += 1
    elif _policy == "COMBO":
        pass
    return reqs

#issue_client_requests([], 5)