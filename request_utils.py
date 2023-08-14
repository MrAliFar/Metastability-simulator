import logging as lg

#### Request types
EXTERNAL = "External"
INTERNAL = "Internal"
ACK = "Ack"
MONITOR = "Monitor"
MONITORRES = "MonitorRespond"

class request:
    def __init__(self, _type, _pattern, _ack_pattern, _origin, _time_slot, _syst_id):
        self.id = -1
        self.syst_id = _syst_id
        self.type = _type
        self.pattern = _pattern
        #### The acknowledgment pattern of the request's communication pattern. It's length
        #### should be one less than the pattern's length.
        self.ack_pattern = _ack_pattern
        #### The original agent from which the request had started. If it is external,
        #### This value will be equal to -1.
        self.origin = _origin
        #### The time slot at which the request is created in the simulation
        self.time_slot = _time_slot
        #### The position of a request in the queue that it resides in. This position
        #### is respecting the end of the queue, i.e., the last element slot. This makes
        #### it easier to use this position as a notion of priority in the event priority queue.
        self.pos = -1
        #### The request's hop number in its communication pattern.
        self.hop = 0
        #### Does this request need a response? This could be set via comparing
        #### the first and final elements of the request's communication pattern.
        self.requires_response = False

def create_request(_type, _pattern, _ack_pattern, _origin, _time_slot, _syst_id):
    """
    The interface between any other piece of code and the request package, for creating
    requests.

    Input: The parameters required to instantiate a request.
    
    Output:
        - A request.
    """
    return request(_type, _pattern, _ack_pattern, _origin, _time_slot, _syst_id)

def create_monitor_request(_type, _origin, _timeslot, _syst_id, _info):
    _req = create_request(request_utils.MONITORRES, Null, Null, NUll, _timeslot, _syst_id)
    _req.monitor_info = _info
    return _req

def copy_request(_req: request):
    _type = _req.type
    _pattern = _req.pattern
    _ack_pattern = _req.ack_pattern
    _origin = _req.origin
    _time_slot = _req.time_slot
    _syst_id = _req.syst_id
    dup_req = request(_type, _pattern, _ack_pattern, _origin, _time_slot, _syst_id)
    return dup_req