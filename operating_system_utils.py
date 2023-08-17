import logging as lg
import request_utils
import event_utils

class operating_system:
    def __init__(self, _syst):
        self.monitor_agent = _syst.monitor_agent
        
    
    def send_monitor_event(_syst, _request, _time):
        
        new_event = event_utils.event(event_utils.SENDING_PRIORITY,
                                            _time,
                                            event_utils.SEND,
                                            _syst.monitor_address[0],
                                            _syst.monitor_address[1],
                                            _request)
        event_utils.insert(_syst.events[_time], new_event)
        return
