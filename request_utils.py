import logging as lg

#### Request types
EXTERNAL = 1
INTERNAL = 2
ACKNOWLEDGEMENT = 3

class request:
    def __init__(self, _type, _pattern, _ack_pattern, _origin, _time_slot):
        self.type = _type
        self.pattern = _pattern
        #### The acknowledgment pattern of the request's communication pattern.
        self.ack_pattern = _ack_pattern
        #### The original agent from which the request had started. If it is external,
        #### This value will be equal to -1.
        self.origin = _origin
        #### The time slot at which the request is created in the simulation
        self.time_slot = _time_slot
        #### The position of a request in the queue that it resides in. This position
        #### is respecting the end of the queue, i.e., the last element slot. This makes
        #### is easier to use this position as a notion of priority in the event priority queue.
        self.pos = -1
        #### Does this request need a response? This could be set via comparing
        #### the first and final elements of the request's communication pattern.
        self.requires_response = False

def create_request(_type, _pattern, _ack_pattern, _origin, _time_slot):
    """
    The interface between any other piece of code and the request package, for creating
    requests.

    Input: The parameters required to instantiate a request.
    
    Output:
        - A request.
    """
    return request(_type, _pattern, _ack_pattern, _origin, _time_slot)