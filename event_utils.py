from random import choice

import logging as lg

import debug_utils

#### Priorities
CLIENT_REQUEST_PRIORITY = 50
SENDING_PRIORITY = 40
PENDING_SERVE_PRIORITY = 30
REQUEST_SERVE_PRIORITY = 20
DUMMY = 0

#### Event types
MEASUREMENT = "Measurement"
SEND = "Send"
CHECK_TIMEOUT = "Check_timeout"
SERVE = "Serve"
FAILURE = "Failure"
CLIENT_REQUEST = "Client_request"
DUMMY_EVENT = "Dummy_event"


class event:
    def __init__(self, _priority, _time, _type, _srvc, _agent, _request):
        #### The priority of the event
        self.priority = _priority
        #### The time slot at which it has to be done, if possible
        self.time = _time
        #### The type of the event
        self.type = _type
        #### The service(s) to which the event belongs
        self.srvc = _srvc
        #### The agent(s) to which the event belongs. If -1, then it is not specified yet.
        self.agent = _agent
        #### The request attached to the event.
        self.request = _request
        #### If the event is a part of a communication pattern, this field tells us the
        #### hop number.
        self.hop = 0

def has_higher_priority(ev1: event, ev2: event):
    if ev1.priority == ev2.priority:
        if ev1.agent == ev2.agent:
            if ev1.priority == REQUEST_SERVE_PRIORITY:
                ev1.request.pos < ev2.request.pos
            elif ev1.priority == PENDING_SERVE_PRIORITY:
                ev1.request.pos < ev2.request.pos
            elif ev1.priority == SENDING_PRIORITY:
                #### TODO:
                pass
            else:
                return ev1.priority < ev2.priority
        else:
            return ev1.priority < ev2.priority
    else:
        return ev1.priority < ev2.priority

def heapify(_arr, n, i):
    # Find the largest among root, left child and right child
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    #if l < n and _arr[i].priority < _arr[l].priority:
    if l < n and has_higher_priority(_arr[i], _arr[l]):
        largest = l

    #if r < n and _arr[largest].priority < _arr[r].priority:
    if r < n and has_higher_priority(_arr[largest], _arr[r]):
        largest = r

    # Swap and continue heapifying if root is not largest
    if largest != i:
        _arr[i], _arr[largest] = _arr[largest], _arr[i]
        heapify(_arr, n, largest)


# Function to insert an element into the tree
def insert(_array, _newEvent):
    size = len(_array)
    if size == 0:
        _array.append(_newEvent)
    else:
        _array.append(_newEvent)
        for i in range((size // 2) - 1, -1, -1):
            heapify(_array, size, i)


# Function to delete an element from the tree
def deleteNode(_array, _event):
    size = len(_array)
    i = 0
    for i in range(0, size):
        if _event == _array[i]:
            break

    _array[i], _array[size - 1] = _array[size - 1], _array[i]

    _array.pop(len(_array)-1)

    for i in range((len(_array) // 2) - 1, -1, -1):
        heapify(_array, len(_array), i)

def issue_client_events(_events, _reqs):
    """
    The interface provided by the events package for populating the event priority queue
    with the initial client request events.

    Input:
        - The events data structure
        - The initial client requests

    Output:
        - The events data structure, containing the initial client request events.
    """
    for req in _reqs:
        insert(_events[req.time_slot], event(CLIENT_REQUEST_PRIORITY, req.time_slot, CLIENT_REQUEST, req.pattern[0], -1, req))
    #return events

def handle_event(_ev, _syst, _cur_time, _sim_len):
    """
    The general event handler. It receives an event and a system, and calls the appropriate
    handler function according to the event's type.
    
    Input:
        - An event.
        - A system
    Output:
        - ?
    """
    if _ev.type == CLIENT_REQUEST:
        return handle_client_request(_ev, _syst, _cur_time, _sim_len)
    elif _ev.type == SERVE:
        return handle_serve_request(_ev, _syst, _cur_time, _sim_len)

def handle_client_request(_ev, _syst, _cur_time, _sim_len):
    #### Put the request inside an agent from the corresponding service. If no agent is
    #### able to handle the request, i.e., all agents have full input queues, drop the
    #### request.
    empty_agent_found = False
    agt_ids = list(range(len(_syst.services[_ev.request.pattern[0]].agents)))
    
    #### Keep randomly looking for an agent that has open capacity in its input queue.
    #### Then assign a serving event to that agent, corresponding to the request.
    while not empty_agent_found:
        agt_id = choice(agt_ids)
        if _syst.services[_ev.request.pattern[0]].agents[agt_id].in_queue.full():
            agt_ids.remove(agt_id)
            continue
        else:
            empty_agent_found = True
            #### The request's position in the agent's input queue. This position is relative to the
            #### last element index. This makes it easier to use the position as a notion of priority.
            _ev.request.pos = _syst.services[_ev.request.pattern[0]].agents[agt_id].in_queue.maxsize - _syst.services[_ev.request.pattern[0]].agents[agt_id].in_queue.qsize()
            _syst.services[_ev.request.pattern[0]].agents[agt_id].in_queue.put(_ev.request)
            incr = _syst.services[_ev.request.pattern[0]].agents[agt_id].in_queue.qsize() // _syst.services[_ev.request.pattern[0]].agents[agt_id].srvc_rate
            if _cur_time + incr > _sim_len-1:
                #### -1 designates that the event belongs to a time after the simulation
                #### length, and we do not have to consider it.
                return -1
            else:
                #### The new serving event corresponding to the request.
                new_event = event(
                    REQUEST_SERVE_PRIORITY,
                    _cur_time + incr,
                    SERVE,
                    _ev.request.pattern[0],
                    agt_id,
                    _ev.request
                )
                #debug_utils.print_unwrapped([new_event])
                return new_event
    #### Add a tentative serving event for the request, assuming that the pending queue
    #### of the chosen agent will remain empty until that time.

def handle_serve_request(_ev, _syst, _cur_time, _sim_len):
    #### Might need to add a pending request in the pending queue.
    if _syst.services[_ev.request.pattern[_ev.request.hop]].agents[_ev.agent]
    #### Handle the request hop.

    #### If served, put the request in the output queue.
    return event(DUMMY, -1, -1, -1, -1, -1)