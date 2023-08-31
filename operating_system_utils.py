import logging as lg
import request_utils
import event_utils

class operating_system:
    def __init__(self):
        return
        
    
    def send_monitor_event(_syst, _request, _time):
        # print("send_monitor_event")
        
        
        destination_out_queue = _syst.services[_syst.monitor_address[0]].agents[_syst.monitor_address[1]].out_queue
        if(destination_out_queue.full()):
            ## change param for more info
            _syst.services[_syst.monitor_address[0]].dropped_monitor_reqs += 1
            return
            
        new_event = event_utils.event(event_utils.SENDING_PRIORITY,
                                            _time,
                                            event_utils.SEND,
                                            _syst.monitor_address[0],
                                            _syst.monitor_address[1],
                                            _request)
        event_utils.insert(_syst.events[_time], new_event)
        destination_out_queue.put(_request)
        return
    
    def send_monitor_respond(_syst, _request, _time, _sev_id, _agt_id ):
        # print("send_monitor_respond")
        destination_out_queue = _syst.services[_sev_id].agents[_agt_id].out_queue
        if(destination_out_queue.full()):
            ## change param for more info
            _syst.services[_syst.monitor_address[0]].dropped_monitor_reqs += 1
            return
        new_event = event_utils.event(event_utils.SENDING_PRIORITY,
                                            _time,
                                            event_utils.SEND,
                                            _sev_id,
                                            _agt_id,
                                            _request)
        event_utils.insert(_syst.events[_time], new_event)
        _syst.services[_sev_id].agents[_agt_id].out_queue.put(_request)
        return
