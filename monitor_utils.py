import template_utils
import random
import logging as lg
import request_utils
import operating_system_utils



###With the assumption of every request would have size, agent have memory..etc 
"""
Monitor class work as application that can operate on multiple agents. 
This monitor routine sends out requests type MONITOR to check how busy they are.
agent respond to this monitor through sending requests with MONITORRESOND type
"""
class monitor:
    def __init__(self, _services):
        self.topology = []
        self.respond_status = [] ##list nestes dic to store curret response / currently store monitor info
        self.current_reqs = []
        self.init_check_ts = 0
        self.agent_list = []
        self.req_id_tracker = 9999 #set large to not duplicate with agents' id
        
        
        for _service in _services:
            templist1 = []
            tempdic1 = dict()
            tempdic2 = dict()
            for _theagent in _service.agents:
                templist1.append(_theagent.id)
                tempdic1[_theagent] = False
                tempdic2[_theagent] = False
            self.topology.append(templist1)
            self.respond_status.append(tempdic1)
            self.current_reqs.append(tempdic2)
        # print(self.topology)
        
        
    
    def start_new_ping_round(self, _syst, _current_timeslot):
        """
        routinely called to give a conclusion of current agents status
        ////currently only called when initializing the system
        """
        self.init_ts = _current_timeslot
        for _service in range(len(self.topology)):
            for _agent in range(len(self.topology[_service])):
                self.current_reqs[_service][_agent] = self.new_monitor_request(_service, _agent, _current_timeslot)
                operating_system_utils.operating_system.send_monitor_event(_syst,self.current_reqs[_service][_agent], _current_timeslot)
    
    def start_new_heartbeat_round(self, _syst, _current_timeslot):
        """
        routinely called to give a conclusion of current agents status
        ////currently only called when initializing the system
        """
        self.init_ts = _current_timeslot
        for _service in range(len(self.topology)):
            for _agent in range(len(self.topology[_service])):
                _theagent = _syst.services[_service].agents[_agent]
                _info = monitor_info.creat_monitor_info(_theagent, _current_timeslot, _current_timeslot)
                self.current_reqs[_service][_agent] = self.new_monitor_request(_service, _agent, _current_timeslot)
                operating_system_utils.operating_system.send_monitor_respond(_syst, self.current_reqs[_service][_agent], _current_timeslot,_service, _agent)

        
    def new_monitor_request(self, _target_service_id, _target_agent_id, _timeslot):
        """
        create a new monitor request with given para
        """
        _info = monitor_info.creat_default_monitor_info( _target_service_id, _target_agent_id, _timeslot)
        temp_req = request_utils.create_monitor_request(
                            request_utils.MONITOR, 
                            _timeslot,
                            self.req_id_tracker,
                            _info
                            )
        # print("new request created" + temp_req.type )
        self.req_id_tracker += 1
        self.current_reqs[_target_service_id][_target_agent_id] = temp_req
        return temp_req
        
        
    def get_response(self, _request):
        """
        Called when the agent recive a request with type MointorRespond
        Would store information inside monitor's memory
        """
        if _request.type != request_utils.MONITORRESPOND:
            lg.info("monitor response have wrong req type")
        else:
            _info = _request._monitor_info
            lg.info("monitor response get" )
            print(str(_info))
            if _info.init_time == self.init_check_ts:
                self.respond_status[_info.from_ser][_info.from_agt] = _info
            
        return
    
    
    def process_monitor_req(self, _ev, _syst, _req, _cur_time):
        """
        with the given event, collect info from hardward and send it back to monitor
        """
        # print("start process event")
        _agent = _syst.services[_ev.srvc].agents[_ev.agent]
        _info = monitor_info.creat_monitor_info(_agent, _req.time_slot, _cur_time)
        print("with "+ str(_info))
        lg.info(_info)
        _new_req = request_utils.create_monitor_request(request_utils.MONITORRESPOND, None, _cur_time ,_info)
        operating_system_utils.operating_system.send_monitor_respond(_syst, _new_req, _cur_time, _ev.srvc, _ev.agent)
        return

class monitor_info:
    def __init__(self):
        self.in_queue_size = 0
        self.out_queue_size = 0
        self.in_queue_ratio = 0
        self.out_queue_ratio = 0
        self.init_time = 0
        self.from_ser = 0
        self.from_agt = 0
        self.arrive_time = 0
        
    def creat_default_monitor_info( _from_ser, _from_agt, _time):
        _info = monitor_info()
        _info.from_ser = _from_ser
        _info.from_agt = _from_agt
        return _info
    
    def creat_monitor_info( _agent, init_time, arrive_time):
        _info = monitor_info()
        _info.in_queue_size = _agent.in_queue.qsize()
        _info.out_queue_size = _agent.out_queue.qsize()
        _info.in_queue_ratio = _agent.in_queue.qsize() / _agent.in_queue.maxsize
        _info.out_queue_ratio = _agent.out_queue.qsize()/ _agent.out_queue.maxsize
        _info.init_time = init_time
        _info.arrive_time = arrive_time
        return _info
        
    def __str__(self):
        return 'INFO: \n in:' + str(self.in_queue_size) + ', out :' +  str(self.out_queue_size) + ' , from: '+ str(self.from_ser) + str(self.from_agt)

def calculate_avg_mem_use(_ev, _syst):
    for _service in _syst.services:
        for _theagent in _service.agents:
            _theagents
            
            
def calculate_avg_queue_use(_ev, _syst):
    for _service in _syst.services:
        for _theagent in _service.agents:
            _theagents