from random import choice
from math import ceil

import logging as lg

import request_utils
import template_utils
import debug_utils

#### Priorities
FAILURE_PRIORITY = 90
MITIGATION_PRIORITY = 80
CLIENT_REQUEST_PRIORITY = 70
SENDING_PRIORITY = 60
RECEIVING_PRIORITY = 50
TIMEOUT_PRIORITY = 40
PENDING_SERVE_PRIORITY = 30
REQUEST_SERVE_PRIORITY = 20
MEASUREMENT_PRIORITY = 10
DUMMY = 0

#### Event types
MEASUREMENT = "Measurement"
SEND = "Send"
RECEIVE = "Receive"
TIMEOUT = "Timeout"
SERVE = "Serve"
FAILURE = "Failure"
MITIGATION = "Mitigation"
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
        #### TODO: Does the hop number belong here? Isn't it better to put it in the requests?
        #### If the event is a part of a communication pattern, this field tells us the
        #### hop number.
        self.hop = 0

def has_higher_priority(ev1: event, ev2: event):
    # if ev1.priority == ev2.priority:
    #     if ev1.agent == ev2.agent:
    #         if ev1.priority == REQUEST_SERVE_PRIORITY:
    #             ev1.request.pos < ev2.request.pos
    #         elif ev1.priority == PENDING_SERVE_PRIORITY:
    #             ev1.request.pos < ev2.request.pos
    #         elif ev1.priority == SENDING_PRIORITY:
    #             #### TODO:
    #             pass
    #         else:
    #             return ev1.priority < ev2.priority
    #     else:
    #         return ev1.priority < ev2.priority
    # else:
    #     return ev1.priority < ev2.priority
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

def issue_measurement_events(_events):
    for i in range(len(_events)):
        meas_event = event(MEASUREMENT_PRIORITY,
                           i,
                           MEASUREMENT,
                           -1,
                           -1,
                           -1)
        insert(_events[i], meas_event)

def issue_failure_events(_events, _failures):
    for failure_inst in _failures:
        failure_event = event(FAILURE_PRIORITY,
                              failure_inst.time,
                              FAILURE,
                              failure_inst.srvc,
                              failure_inst.agent,
                              failure_inst)
        insert(_events[failure_event.time], failure_event)

def issue_mitigation_events(_events, _mitigations):
    for mitigation_inst in _mitigations:
        mitigation_event = event(MITIGATION_PRIORITY,
                              mitigation_inst.time,
                              MITIGATION,
                              mitigation_inst.srvc,
                              mitigation_inst.agent,
                              mitigation_inst)
        insert(_events[mitigation_event.time], mitigation_event)

def handle_event(_ev, _syst, _cur_time, _network_delay, _sim_len):
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
        return handle_client_request(_ev, _syst, _cur_time, _network_delay, _sim_len)
    elif _ev.type == SERVE:
        return handle_serve_event(_ev, _syst, _sim_len)
    elif _ev.type == RECEIVE:
        return handle_receive_event(_ev, _syst)
    elif _ev.type == SEND:
        return handle_send_event(_ev, _syst, _network_delay, _sim_len)
    elif _ev.type == MEASUREMENT:
        return handle_measurement_event(_syst, _cur_time)
    elif _ev.type == FAILURE:
        return handle_failure_event(_ev, _syst)
    elif _ev.type == MITIGATION:
        return handle_mitigation_event(_ev, _syst)
    elif _ev.type == TIMEOUT:
        return handle_timeout_event(_ev, _syst, _sim_len)

def handle_client_request(_ev, _syst, _cur_time, _network_delay, _sim_len):
    #### Select a random agent from the corresponding service.
    agt_ids = list(range(len(_syst.services[_ev.request.pattern[0]].agents)))
    agt_id = choice(agt_ids)
            
    if _cur_time + _network_delay > _sim_len-1:
        #### -1 designates that the event belongs to a time after the simulation
        #### length, and we do not have to consider it.
        #### TODO: Does returning -1 universally capture everything?
        return -1
    else:
        #### The new receiving event corresponding to the request.
        _ev.request.origin = agt_id
        new_event = event(
            RECEIVING_PRIORITY,
            _cur_time + _network_delay,
            RECEIVE,
            _ev.request.pattern[0],
            agt_id,
            _ev.request
        )
        #debug_utils.print_unwrapped([new_event])
        return [new_event]

def handle_serve_event(_ev, _syst, _sim_len):
    #### Might need to add a pending request in the pending queue.
    out_queue_is_full = False
    new_event = -1
    new_events = []
    leftover_serve_event = -1
    while not out_queue_is_full:
        if _syst.services[_ev.srvc].agents[_ev.agent].out_queue.full():
            out_queue_is_full = True
            continue
        else:
            in_queue_is_empty = False
            while not in_queue_is_empty:
                if _syst.services[_ev.srvc].agents[_ev.agent].in_queue.empty():
                    in_queue_is_empty = True
                    out_queue_is_full = True
                    continue
                else:
                    #for _ in range(_syst.services[_ev.srvc].agents[_ev.agent].srvc_rate):
                    while _syst.services[_ev.srvc].agents[_ev.agent].remaining_srvc > 0:
                        lg.info("Served!")
                        #### TODO: We need this request to handle timeouts. For now, we do not have timeouts.

                        #### Get the next request in the queue.
                        #lg.info(f"Behind the queue - srvc is {_ev.srvc} - agent is {_ev.agent}")
                        req = _syst.services[_ev.srvc].agents[_ev.agent].in_queue.get()
                        #### Update the online service capacity.
                        _syst.services[_ev.srvc].agents[_ev.agent].remaining_srvc += -1
                        if req.type == request_utils.ACK:
                            #lg.info("ACK!")
                            for requ in _syst.services[_ev.srvc].agents[_ev.agent].pending_bag:
                                if requ.id == req.id:
                                    lg.info(f"Removed!! srvc is {_ev.srvc} - agent is {_ev.agent} - id is {requ.id} - len is {len(_syst.services[_ev.srvc].agents[_ev.agent].pending_bag)}")
                                    _syst.services[_ev.srvc].agents[_ev.agent].pending_bag.remove(requ)
                                    lg.info(f"len after remove is {len(_syst.services[_ev.srvc].agents[_ev.agent].pending_bag)}")
                                    requ.id = -1
                                    break
                            if _syst.services[_ev.srvc].agents[_ev.agent].out_queue.full():
                                in_queue_is_empty = True
                                out_queue_is_full = True
                                break
                            if _syst.services[_ev.srvc].agents[_ev.agent].in_queue.empty():
                                in_queue_is_empty = True
                                out_queue_is_full = True
                                break
                            continue
                        if req.hop > 0:
                            #lg.info(f"Inside req.hop > 0 - time is {_ev.time} - ack_pattern is {req.ack_pattern} - hop is {req.hop}")
                            if req.ack_pattern[req.hop - 1] == 1:
                                #lg.info(f"Need to respond - time is {_ev.time} - pattern is {req.pattern} - hop is {req.hop} - origin is {req.origin}")
                                ack_req = request_utils.create_request(request_utils.ACK,
                                                                [-1, req.pattern[req.hop - 1]],
                                                                [],
                                                                req.origin,
                                                                _ev.time)
                                ack_req.id = req.id
                                _syst.services[_ev.srvc].agents[_ev.agent].out_queue.put(ack_req)
                                if not _ev.time in _syst.services[_ev.srvc].agents[_ev.agent].send_events:
                                    new_event = event(SENDING_PRIORITY,
                                                    _ev.time,
                                                    SEND,
                                                    _ev.srvc,
                                                    _ev.agent,
                                                    -1)
                                    new_events.append(new_event)
                                    _syst.services[_ev.srvc].agents[_ev.agent].send_events[_ev.time] = True
                        if not req.hop == len(req.pattern)-1:
                            #lg.info("Not the last hop!")
                            if req.ack_pattern[req.hop] == 1:
                                if len(_syst.services[_ev.srvc].agents[_ev.agent].pending_bag) < _syst.services[_ev.srvc].agents[_ev.agent].pending_bag_cap:
                                    pending_req = request_utils.copy_request(req)
                                    req.origin = _ev.agent
                                    
                                    #### Unique timestamp to recognize later, when receiving the ack
                                    req.id = _syst.services[_ev.srvc].agents[_ev.agent].timeout_index_cntr
                                    pending_req.id = _syst.services[_ev.srvc].agents[_ev.agent].timeout_index_cntr
                                    _syst.services[_ev.srvc].agents[_ev.agent].timeout_index_cntr += 1

                                    _syst.services[_ev.srvc].agents[_ev.agent].pending_bag.append(pending_req)
                                    timeout_slot = _ev.time + _syst.services[_ev.srvc].agents[_ev.agent].timeout
                                    if not timeout_slot > _sim_len - 1:
                                        timeout_event = event(TIMEOUT_PRIORITY,
                                                            timeout_slot,
                                                            TIMEOUT,
                                                            _ev.srvc,
                                                            _ev.agent,
                                                            pending_req)
                                        new_events.append(timeout_event)
                                else:
                                    #### TODO: Check this!
                                    lg.info(f"Dropped! Full pending. cap is {_syst.services[_ev.srvc].agents[_ev.agent].pending_bag_cap}")
                                    _syst.services[_ev.srvc].dropped_reqs += 1
                                    _syst.services[_ev.srvc].agents[_ev.agent].dropped_reqs += 1
                                    if _syst.services[_ev.srvc].agents[_ev.agent].out_queue.full():
                                        in_queue_is_empty = True
                                        out_queue_is_full = True
                                        break
                                    if _syst.services[_ev.srvc].agents[_ev.agent].in_queue.empty():
                                        in_queue_is_empty = True
                                        out_queue_is_full = True
                                        break
                                    continue
                            #else:
                            if not _ev.time in _syst.services[_ev.srvc].agents[_ev.agent].send_events:
                                new_event = event(SENDING_PRIORITY,
                                                _ev.time,
                                                SEND,
                                                _ev.srvc,
                                                _ev.agent,
                                                -1)
                                new_events.append(new_event)
                                _syst.services[_ev.srvc].agents[_ev.agent].send_events[_ev.time] = True
                                #### Put the request in the output queue.
                            _syst.services[_ev.srvc].agents[_ev.agent].out_queue.put(req)
                        else:
                            #### If the request is in its final hop, then no need to create
                            #### a send event.

                            #### TODO: Check this!
                            del req
                        if _syst.services[_ev.srvc].agents[_ev.agent].out_queue.full():
                            in_queue_is_empty = True
                            out_queue_is_full = True
                            break
                        if _syst.services[_ev.srvc].agents[_ev.agent].in_queue.empty():
                            in_queue_is_empty = True
                            out_queue_is_full = True
                            break
                    in_queue_is_empty = True
                    out_queue_is_full = True
        #out_queue_is_full = _syst.services[_ev.srvc].agents[_ev.agent].out_queue.full()
    #### If there are requests remaining in the input queue, the agent should
    #### serve at the next time slot.
    if not _syst.services[_ev.srvc].agents[_ev.agent].in_queue.empty():
        if not _ev.time + 1 > _sim_len - 1:
            if not _ev.time + 1 in _syst.services[_ev.srvc].agents[_ev.agent].serve_events:
                leftover_serve_event = event(REQUEST_SERVE_PRIORITY,
                                            _ev.time + 1,
                                            SERVE,
                                            _ev.srvc,
                                            _ev.agent,
                                            -1)
                new_events.append(leftover_serve_event)
                _syst.services[_ev.srvc].agents[_ev.agent].serve_events[_ev.time + 1] = True
    #### Reset the online serving capacity.
    _syst.services[_ev.srvc].agents[_ev.agent].remaining_srvc = _syst.services[_ev.srvc].agents[_ev.agent].srvc_rate
    return new_events


def handle_receive_event(_ev, _syst):
    #### If the request does not have an agent specified, then this handler chooses
    #### a random agent from the corresponding agent, and assigns the event to this
    #### randomly selected agent.
    if _ev.agent == "Random":
        agt_ids = list(range(len(_syst.services[_ev.srvc].agents)))
        _ev.agent = choice(agt_ids)
    
    #### Check to see whether the request has to be dropped.
    if _syst.services[_ev.srvc].agents[_ev.agent].in_queue.full():
        #### TODO: Handle dropping.
        lg.info(f"request dropped: {vars(_ev.request)}")
        _syst.services[_ev.srvc].dropped_reqs += 1
        _syst.services[_ev.srvc].agents[_ev.agent].dropped_reqs += 1
        return -1
    else:
        #### The request's position in the agent's input queue. This position is relative to the
        #### last element index. This makes it easier to use the position as a notion of priority.
        _ev.request.pos = _syst.services[_ev.srvc].agents[_ev.agent].in_queue.maxsize - _syst.services[_ev.srvc].agents[_ev.agent].in_queue.qsize()
        #lg.info(f"Receive--Put - Input queue of agent {_ev.agent} in service {_ev.srvc}")
        _syst.services[_ev.srvc].agents[_ev.agent].in_queue.put(_ev.request)
        if not _ev.time in _syst.services[_ev.srvc].agents[_ev.agent].serve_events:
            new_event = event(REQUEST_SERVE_PRIORITY,
                              _ev.time,
                              SERVE,
                              _ev.srvc,
                              _ev.agent,
                              -1)
            _syst.services[_ev.srvc].agents[_ev.agent].serve_events[_ev.time] = True
            return [new_event]
        else:
            #### TODO: Should returning -1 universally capture everything?
            return -1

def handle_send_event(_ev, _syst, _network_delay, _sim_len):
    #### TODO: the following returns very early. Perhaps the delays are different for each
    #### request in the output queue.
    if _ev.time + _network_delay > _sim_len - 1:
        return -1
    out_queue_is_empty = False
    new_events = []
    while not out_queue_is_empty:
        for _ in range(_syst.services[_ev.srvc].agents[_ev.agent].send_rate):
            #lg.info(f"Send--Get - Input queue of agent {_ev.agent} in service {_ev.srvc}")
            req = _syst.services[_ev.srvc].agents[_ev.agent].out_queue.get()
            req.hop = req.hop + 1
            if req.type == request_utils.EXTERNAL:
                #lg.info(f"send event - time is {_ev.time} - pattern is {req.pattern} - hop is {req.hop} - srvc is {_ev.srvc}")
                new_event = event(RECEIVING_PRIORITY,
                                _ev.time + _network_delay,
                                RECEIVE,
                                req.pattern[req.hop],
                                "Random",
                                req)
            elif req.type == request_utils.ACK:
                #lg.info(f"Sending ack - srvc is {req.pattern[req.hop]} - agent is {req.origin}")
                new_event = event(RECEIVING_PRIORITY,
                                _ev.time + _network_delay,
                                RECEIVE,
                                req.pattern[req.hop],
                                req.origin,
                                req)
            new_events.append(new_event)
            if _syst.services[_ev.srvc].agents[_ev.agent].out_queue.empty():
                out_queue_is_empty = True
                break
        out_queue_is_empty = True
    if not _syst.services[_ev.srvc].agents[_ev.agent].out_queue.empty():
        if not _ev.time + 1 > _sim_len - 1:
            if not _ev.time + 1 in _syst.services[_ev.srvc].agents[_ev.agent].send_events:
                left_over_send_event = event(SENDING_PRIORITY,
                                            _ev.time + 1,
                                            SEND,
                                            _ev.srvc,
                                            _ev.agent,
                                            -1)
                new_events.append(left_over_send_event)
                _syst.services[_ev.srvc].agents[_ev.agent].send_events[_ev.time + 1] = True
    return new_events
            
    #### Handle the request hop.

def handle_measurement_event(_syst, _cur_time):
    num_dropped = 0
    for i in range(len(_syst.services)):
        num_dropped += _syst.services[i].dropped_reqs
    _syst.dropped_reqs.append(num_dropped)
    lg.info(f"The number of dropped requests in time {_cur_time} is {num_dropped}")
    return -1

def handle_failure_event(_ev, _syst):
    if _ev.request.type == "DEGRADE":
        _syst.services[_ev.srvc].agents[_ev.agent].srvc_rate = ceil(_syst.services[_ev.srvc].agents[_ev.agent].srvc_rate * _ev.request.degradation_factor)
    elif _ev.request.type == "CRASH":
        _syst.services[_ev.srvc].agents[_ev.agent].srvc_rate = 0
    #### TODO: Does -1 universally capture everything?
    return -1

def handle_mitigation_event(_ev, _syst):
    if _ev.request.type == "UPGRADE":
        pass
    elif _ev.request.type == "REVIVE":
        _syst.services[_ev.srvc].agents[_ev.agent].srvc_rate = _syst.services[_ev.srvc].agents[_ev.agent].original_srvc_rate
    #### TODO: Does -1 universally capture everything?
    return -1

def handle_timeout_event(_ev, _syst, _sim_len):
    #### TODO: Fill this function.
    new_events = []
    if _ev.request.id < 0:
        return new_events
    if _syst.services[_ev.srvc].agents[_ev.agent].remaining_srvc > 0:
        if not _syst.services[_ev.srvc].agents[_ev.agent].out_queue.full():
            if not _ev.time in _syst.services[_ev.srvc].agents[_ev.agent].send_events:
                _syst.services[_ev.srvc].agents[_ev.agent].send_events[_ev.time] = True
                send_event = event(SENDING_PRIORITY,
                                   _ev.time,
                                   SEND,
                                   _ev.srvc,
                                   _ev.agent,
                                   -1)
                new_events.append(send_event)
            send_req = request_utils.copy_request(_ev.request)
            _syst.services[_ev.srvc].agents[_ev.agent].out_queue.put(send_req)
            timeout_slot = _ev.time + _syst.services[_ev.srvc].agents[_ev.agent].timeout
            if not timeout_slot > _sim_len - 1:
                timeout_event = event(TIMEOUT_PRIORITY,
                                      timeout_slot,
                                      TIMEOUT,
                                      _ev.srvc,
                                      _ev.agent,
                                      _ev.request)
                new_events.append(timeout_event)
        else:
            timeout_slot = _ev.time + 1
            if not timeout_slot > _sim_len - 1:
                timeout_event = event(TIMEOUT_PRIORITY,
                                      timeout_slot,
                                      TIMEOUT,
                                      _ev.srvc,
                                      _ev.agent,
                                      _ev.request)
                new_events.append(timeout_event)
        _syst.services[_ev.srvc].agents[_ev.agent].remaining_srvc += -1
    else:
        timeout_slot = _ev.time + 1
        if not timeout_slot > _sim_len - 1:
            timeout_event = event(TIMEOUT_PRIORITY,
                                  timeout_slot,
                                  TIMEOUT,
                                  _ev.srvc,
                                  _ev.agent,
                                  _ev.request)
            new_events.append(timeout_event)
    if not _ev.time in _syst.services[_ev.srvc].agents[_ev.agent].serve_events:
        _syst.services[_ev.srvc].agents[_ev.agent].serve_events[_ev.time] = True
        serve_event = event(REQUEST_SERVE_PRIORITY,
                           _ev.time,
                           SERVE,
                           _ev.srvc,
                           _ev.agent,
                           -1)
        new_events.append(serve_event)
    return new_events