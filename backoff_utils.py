import template_utils

import logging as lg


def calculate_timeoutslot(_ev, _syst):
    
    """
    A function that calculates corresponding future timeoutslot base on current backoff policy
    
    Input:
        - ev: The event that potentially timeout in the future
        - syst: current system setting
    Output:
        - the next timeout slot number
    """
    

    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "MUL":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = _syst.services[_ev.srvc].agents[_ev.agent].timeout * 2
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "ADD":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = _syst.services[_ev.srvc].agents[_ev.agent].timeout + 1
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "RAND":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = _syst.services[_ev.srvc].agents[_ev.agent].timeout * 2
        return _ev.time + random.randint( 1 , _syst.services[_ev.srvc].agents[_ev.agent].timeout)
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "BUCK":
        if _syst.services[_ev.srvc].agents[_ev.agent].timeout_bucket < 0 : 
            #### 
            return 0
    
    return _ev.time + _syst.services[_ev.srvc].agents[_ev.agent].timeout


