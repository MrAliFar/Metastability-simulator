import template_utils
import random

import logging as lg
def calculate_timeoutslot(_ev, _syst):
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "RAND":
        return _ev.time + random.randint( 1 , _syst.services[_ev.srvc].agents[_ev.agent].timeout)
    else:
        return _ev.time + _syst.services[_ev.srvc].agents[_ev.agent].timeout

def timeout_backoff(_ev, _syst):
    
    """
    A function that calculates corresponding future timeoutslot base on current backoff policy
    
    Input:
        - ev: The event that potentially timeout in the future
        - syst: current system setting
    Output:
        - the next timeout slot number
    """
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "EXP":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = _syst.services[_ev.srvc].agents[_ev.agent].timeout * 2
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "LIN":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = _syst.services[_ev.srvc].agents[_ev.agent].timeout + 1
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "RAND":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = _syst.services[_ev.srvc].agents[_ev.agent].timeout * 2
        return _ev.time + random.randint( 1 , _syst.services[_ev.srvc].agents[_ev.agent].timeout)
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "BUCK":
        if _syst.services[_ev.srvc].agents[_ev.agent].timeout_bucket < 0 : 
            #### TODO: would return 0 safe
            return 0
        else :
            _syst.services[_ev.srvc].agents[_ev.agent].timeout_bucket -= 1
    
    return _ev.time + _syst.services[_ev.srvc].agents[_ev.agent].timeout



def timeout_change_newtimeslot( _syst):
    for _service in _syst.services:
        for _theagent in _service.agents:
            if _theagent.backoff_behavior == "BUCK":
                _theagent.timeout_bucket += 2


def request_success_timeout_change(_ev, _syst):
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "BUCK":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout_bucket +=1
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "EXP":
        if _syst.services[_ev.srvc].agents[_ev.agent].timeout > 5: 
            _syst.services[_ev.srvc].agents[_ev.agent].timeout -= 3
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "RAND":
        ##currently too small decrease so actually slowing down agents
        if _syst.services[_ev.srvc].agents[_ev.agent].timeout > 5: 
            _syst.services[_ev.srvc].agents[_ev.agent].timeout -= 3
    
        
