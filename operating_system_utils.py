import logging as lg
import request_utils
import event_utils

class operating_system:
    def __init__(self):
        return
        
    
    def send_monitor_event(_syst, _request, _time):
        # print("send_monitor_event")
        new_event = event_utils.event(event_utils.SENDING_PRIORITY,
                                            _time,
                                            event_utils.SEND,
                                            _syst.monitor_address[0],
                                            _syst.monitor_address[1],
                                            _request)
        event_utils.insert(_syst.events[_time], new_event)
        _syst.services[_syst.monitor_address[0]].agents[_syst.monitor_address[1]].out_queue.put(_request)
        return
    
    def send_monitor_respond(_syst, _request, _time, _ev ):
        # print("send_monitor_respond")
        new_event = event_utils.event(event_utils.SENDING_PRIORITY,
                                            _time,
                                            event_utils.SEND,
                                            _ev.srvc,
                                            _ev.agent,
                                            _request)
        event_utils.insert(_syst.events[_time], new_event)
        _syst.services[_ev.srvc].agents[_ev.agent].out_queue.put(_request)
        return
