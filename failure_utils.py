import template_utils

import logging as lg

class failure:
    def __init__(self, _srvc, _agent, _time, _degradation_factor, _type):
        self.srvc = _srvc
        self.agent = _agent
        self.time = _time
        self.degradation_factor = _degradation_factor
        self.type = _type

def get_failures():
    failures = []
    failure_lsts = template_utils.parse_failures()
    lg.info(f"failures are {failure_lsts}")
    for failure_lst in failure_lsts:
        new_failure = failure(failure_lst[0],
                              failure_lst[1],
                              failure_lst[2],
                              failure_lst[3],
                              failure_lst[4])
        failures.append(new_failure)
    return failures