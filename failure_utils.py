import template_utils

import logging as lg

class failure:
    def __init__(self, _srvc, _agent, _time, _degradation_factor, _type):
        self.srvc = _srvc
        self.agent = _agent
        self.time = _time
        self.degradation_factor = _degradation_factor
        self.type = _type

class mitigation:
    def __init__(self, _srvc, _agent, _time, _mitigation_factor, _type):
        self.srvc = _srvc
        self.agent = _agent
        self.time = _time
        self.mitigation_factor = _mitigation_factor
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

def get_mitigations():
    mitigations = []
    mitigation_lsts = template_utils.parse_mitigations()
    lg.info(f"mitigations are {mitigation_lsts}")
    for mitigation_lst in mitigation_lsts:
        new_mitigation = mitigation(mitigation_lst[0],
                              mitigation_lst[1],
                              mitigation_lst[2],
                              mitigation_lst[3],
                              mitigation_lst[4])
        mitigations.append(new_mitigation)
    return mitigations