import template_utils
import random
import logging as lg
import request_utils
import operating_system_utils


srvc_rate_cost = 1
agent_max_garbage = 10

###Simulate a working garbage collector 
"""
The class defines the garbage collection behavior 
"""
def start_garbage_collect(_agent):
    ### simulat the effect of garbage collector 
    if _agent.remaining_srvc == 0:
        return
    _agent.remaining_srvc -= srvc_rate_cost
    _agent.garbage_counter = 0
    

def check_garbage_status(_agent):
    # print(_agent.garbage_collect)
    if not _agent.garbage_collect:
        return
    # print("gc called")
    if _agent.garbage_counter >= agent_max_garbage:
        start_garbage_collect(_agent)

def count_garbage(_agent):
    ### currently set to 1 but would need to be modifiy in the future
    _agent.garbage_counter +=1
