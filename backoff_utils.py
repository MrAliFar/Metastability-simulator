import template_utils
import random

import logging as lg
def calculate_timeoutslot(_ev, _syst):
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "RAND":
        return _ev.time + random.randint(5 , _syst.services[_ev.srvc].agents[_ev.agent].timeout)
    else:
        return _ev.time + _syst.services[_ev.srvc].agents[_ev.agent].timeout

def timeout_backoff(_ev, _syst):
    timeout_backoff_t(_ev.srvc, _ev.agent, _syst)

def add_timeout_backoff(_ev, _syst):
    _serv = _ev.srvc
    _agent = _ev.agent
    _syst.services[_serv].agents[_agent].timeout = min(_syst.services[_serv].agents[_agent].timeout + 4, 30)

def exp_timeout_backoff(_ev, _syst):
    _serv = _ev.srvc
    _agent = _ev.agent
    _syst.services[_serv].agents[_agent].timeout = min(_syst.services[_serv].agents[_agent].timeout * 2, 30)


    
def timeout_backoff_t(_serv, _agent, _syst):
    
    """
    A function that modifies backoff  base on current backoff policy
    
    Input:
        - ev: The event that potentially timeout in the future
        - syst: current system setting
    Output:
        - the next timeout slot number
    """
    if _syst.services[_serv].agents[_agent].backoff_behavior == "EXP":
        _syst.services[_serv].agents[_agent].timeout = min(_syst.services[_serv].agents[_agent].timeout * 2, 30)
    if _syst.services[_serv].agents[_agent].backoff_behavior == "ADD":
        _syst.services[_serv].agents[_agent].timeout = min(_syst.services[_serv].agents[_agent].timeout + 4, 30)
    if _syst.services[_serv].agents[_agent].backoff_behavior == "RAND":
        _syst.services[_serv].agents[_agent].timeout = min(_syst.services[_serv].agents[_agent].timeout * 2, 30)
    if _syst.services[_serv].agents[_agent].backoff_behavior == "BUCK":
        if _syst.services[_serv].agents[_agent].timeout_bucket < 0 : 
            return 0
        else:
            """timeout must be at least in the future"""
            _syst.services[_serv].agents[_agent].timeout_bucket -= 1



def timeout_change_newtimeslot( _syst):
    for _service in _syst.services:
        for _theagent in _service.agents:
            if _theagent.backoff_behavior == "BUCK":
                _theagent.timeout_bucket += 2


def request_success_timeout_change(_ev, _syst):
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "BUCK":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout_bucket +=1
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "EXP": 
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = max(5, _syst.services[_ev.srvc].agents[_ev.agent].timeout -3)
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "RAND":
        ##currently too small decrease so actually slowing down agents
        if _syst.services[_ev.srvc].agents[_ev.agent].timeout > 5: 
            _syst.services[_ev.srvc].agents[_ev.agent].timeout -= 3
    if _syst.services[_ev.srvc].agents[_ev.agent].backoff_behavior == "ADD":
        _syst.services[_ev.srvc].agents[_ev.agent].timeout = max(5,_syst.services[_ev.srvc].agents[_ev.agent].timeout -1 )
    
        
