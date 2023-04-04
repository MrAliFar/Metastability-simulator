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
    if _policy == "AUTO":
        #### Issue requests selected uniformly at random from the parsed
        #### requests. The requests differ based on their communication pattern.
        reqs = []
        for _ in range(num_reqs):
            ts = randint(0, sim_len - 1)
            pattern_index = randint(0, len(req_patterns) - 1)
            reqs.append(request_utils.create_request(request_utils.EXTERNAL, req_patterns[pattern_index], req_acks[pattern_index], -1, ts))
    else:
        #### Manual generation of requests. This will be handy when studying the effect
        #### of load-increasing events.
        reqs = generate_requests()

    return reqs

#### TODO:
def generate_requests():
    pass

#issue_client_requests([], 5)