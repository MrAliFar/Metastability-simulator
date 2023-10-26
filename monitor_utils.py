import template_utils
import random
import logging as lg
import request_utils
import operating_system_utils
import backoff_utils
import system_utils



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
        self.active = False
        self.active_control = 0
        self.record = []
        self.record_in_num = [] ## currently setin the form of [ [served_req_num, retried_req_num at time x], [served_req_num, retried_req_num at time x+k], ...]
        
        for _service in _services:
            num_agt = len(_service.agents)
            templist1 = []
            tempdic1 = []
            tempdic2 = []
            for _theagent in range(num_agt):
                templist1.append(_service.agents[_theagent].id)
                tempdic1.append(monitor_info.create_default_monitor_info(_service, _theagent, -1))
                tempdic2.append([])
            self.topology.append(templist1)
            self.respond_status.append(tempdic1)
            self.current_reqs.append(tempdic2)

    def start_new_ping_round(self, _syst, _current_timeslot):
        """
        routinely called to give a conclusion of current agents status
        """
        if not self.active:
            return
        self.init_ts = _current_timeslot
        for _service in range(len(self.topology)):
            for _agent in range(len(self.topology[_service])):
                self.current_reqs[_service][_agent] = self.new_monitor_request(_service, _agent, _current_timeslot)
                operating_system_utils.operating_system.send_monitor_event(_syst,self.current_reqs[_service][_agent], _current_timeslot)
    
    def start_new_heartbeat_round(self, _syst, _current_timeslot):
        """
        routinely called to give a conclusion of current agents status
        """
        if not self.active:
            return
        self.store_info()
        self.init_ts = _current_timeslot
        for _service in range(len(self.topology)):
            for _agent in range(len(self.topology[_service])):
                _theagent = _syst.services[_service].agents[_agent]
                _info = monitor_info.create_monitor_info(_service, _agent, _theagent, _current_timeslot, _current_timeslot)
                self.current_reqs[_service][_agent] = self.new_monitor_request(_service, _agent, _current_timeslot)
                operating_system_utils.operating_system.send_monitor_respond(_syst, self.current_reqs[_service][_agent], _current_timeslot,_service, _agent)

        
    def new_monitor_request(self, _target_service_id, _target_agent_id, _timeslot):
        """
        create a new monitor request with given para
        """
        _info = monitor_info.create_default_monitor_info( _target_service_id, _target_agent_id, _timeslot)
        temp_req = request_utils.create_monitor_request(
                            _timeslot,
                            self.req_id_tracker,
                            _info
                            )
        self.req_id_tracker += 1
        self.current_reqs[_target_service_id][_target_agent_id] = temp_req
        return temp_req
        
        
    def get_response(self, _request, _syst):
        """
        Called when the agent recive a request with type MointorRespond
        Would store information inside monitor's memory
        """
        if _request.type != request_utils.MONITOR_RESPOND:
            lg.info("monitor response have wrong req type")
        else:
            _info = _request.monitor_info
            lg.info("monitor response get" )
            lg.info(str(_info))
            # if _info.init_time == self.init_check_ts:
            self.respond_status[_info.from_ser][_info.from_agt] = _info
            self.active_monitor_control(_syst, _info)
        return
    
    def store_info(self):
        templist = []
        served_req_dif = 0
        retried_req_dif = 0
        lastelem = []
        if(len(self.record) > 1 ):
            lastelem = self.record[len(self.record)-1]
        
        # print("new round, dif is ") 
        for i in range(len(self.respond_status)):
            templist.append(self.respond_status[i].copy())
            for j in range( len(self.respond_status[i])):
                # print(j ,"agt retry" , self.respond_status[i][j].retried_req_num)
                served_req_dif +=  self.respond_status[i][j].responded_req_num
                retried_req_dif += self.respond_status[i][j].retried_req_num
                if(len(self.record) > 1 ):
                    served_req_dif -= lastelem[i][j].responded_req_num
                    retried_req_dif -= lastelem[i][j].retried_req_num
                # print( str(retried_req_dif) +"   "+ str(j))
        lg.info(served_req_dif)
        lg.info(retried_req_dif)
        # print( served_req_dif)
        # print( retried_req_dif)
        
        self.record.append(templist)
        
        return
    
    def process_monitor_req(self, _ev, _syst, _req, _cur_time):
        """
        with the given event, collect info from hardward and send it back to monitor
        """
        _agent = _syst.services[_ev.srvc].agents[_ev.agent]
        _info = monitor_info.create_monitor_info(_ev.srvc, _ev.agent, _agent, _req.time_slot, _cur_time)
        lg.info(_info)
        _new_req = request_utils.create_monitor_respond_request( _cur_time, _info)
        operating_system_utils.operating_system.send_monitor_respond(_syst, _new_req, _cur_time, _ev.srvc, _ev.agent)
        return
    
    def active_monitor_control(self, _syst, _info):
        ###
        # If the monitor is actively in load control, modify timout for corresponding notes
        if(self.active == False):
            return
        if(self.active_control == 0):
        ### active monitor but no active control
            return
        is_busy = False
        if(self.active_control == 1):
            is_busy = self.check_busyness_1(_info)
        if(self.active_control == 2):
            is_busy = self.check_busyness_2(_info)
            
        if(is_busy):
            if(_info.from_ser == _syst.monitor_address[0] and _info.from_agt == _syst.monitor_address[1]):
                backoff_utils.timeout_backoff_t( _info.from_ser,_info.from_agt, _syst)
            else:
                ###schedule a send
                _change = monitor_change.create_default_monitor_change(3, 0, _info.from_ser, _info.from_agt)
                # print("change is " + str(_change))
                lg.info(str(_change))
                new_req = request_utils.create_monitor_change_request( _syst.time,  _change)
                operating_system_utils.operating_system.default_send(
                    _syst, new_req, _syst.time, _syst.monitor_address[0],_syst.monitor_address[0], _info.from_ser, _info.from_agt)
        
    def monitor_process(self, _ev, _syst, _req, _cur_time):
        if _req.type == request_utils.MONITOR:
            self.process_monitor_req(_ev, _syst, _req, _cur_time)
            _syst.services[_ev.srvc].agents[_ev.agent].served_monitor_req += 1
            _syst.services[_ev.srvc].agents[_ev.agent].served_reqs -= 1
        elif _req.type == request_utils.MONITOR_RESPOND:
            _syst.monitor.get_response(_req, _syst)
        elif _req.type == request_utils.CHANGE:
            # print("get a change req")
            monitor_change.process_monitor_change(_syst, _req.monitor_change)
        
    def check_busyness_1(self, _info):
        ### """check if the given info shows sign that they are busy"""
        if(_info.memory_ratio > 0.8):
            return True

        return False
    
    def check_busyness_2(self, _info):
        if(_info.in_queue_ratio > 0.8):
            return True
        return False
    
    def check_busyness_3(self, _info):
        ### try to check tail laentency for each agent
        if(_info.out_queue_ratio > 0.8):
            return
        return False
        
        
class monitor_info:
    def __init__(self):
        self.in_queue_size = 0
        self.out_queue_size = 0
        self.in_queue_ratio = 0
        self.out_queue_ratio = 0
        self.memory_ratio = 0
        self.init_time = 0
        self.from_ser = 0
        self.from_agt = 0
        self.arrive_time = 0
        self.responded_req_num =0
        self.retried_req_num =0
        
    def create_default_monitor_info( _from_ser, _from_agt, _time):
        _info = monitor_info()
        _info.from_ser = _from_ser
        _info.from_agt = _from_agt
        return _info
    
    def create_monitor_info(_from_ser, _from_agt, _agent, init_time, arrive_time):
        _info = monitor_info()
        _info.from_ser = _from_ser
        _info.from_agt = _from_agt
        _info.in_queue_size = _agent.in_queue.qsize()
        _info.out_queue_size = _agent.out_queue.qsize()
        _info.in_queue_ratio = float(_agent.in_queue.qsize()) / _agent.in_queue.maxsize
        _info.out_queue_ratio = float(_agent.out_queue.qsize())/ _agent.out_queue.maxsize
        _info.init_time = init_time
        _info.arrive_time = arrive_time
        _info.memory_ratio = float(len(_agent.pending_bag))/_agent.pending_bag_cap
        _info.responded_req_num =  _agent.responded_reqs
        # print("num of retried is " + str(_agent.retried_reqs))
        _info.retried_req_num = _agent.retried_reqs
        return _info
        
    def __str__(self):
        return 'INFO: \n in:' + str(self.in_queue_size) + ', out :' +  str(self.out_queue_size) +',memory :' + str(self.memory_ratio) + ' , from: '+ str(self.from_ser) + str(self.from_agt)

class monitor_change:
    def __init__(self):
        ### supported things to change
        self.backoff = 0
        self.drop_pending = 0
        ### info for identity
        self.target_ser = 0
        self.target_agt = 0
    
    def create_default_monitor_change(b_change, d_change, to_ser,  to_agt):
        _change = monitor_change()
        _change.backoff = b_change
        _change.drop_pending = d_change
        _change.target_ser = to_ser
        _change.target_agt = to_agt
        return _change

    def process_monitor_change(_syst, _change):
        _agent = _syst.services[_change.target_ser].agents[_change.target_agt]
        _agent.timeout = max(5,_agent.timeout - _change.backoff)
        if(_change.drop_pending !=0):
            ### do something
            pass
    
    def __str__(self):
        return 'CHANGE: \n backoff:' + str(self.backoff) + ', drop :' +  str(self.drop_pending) +',from:' +str(self.target_ser) + str(self.target_agt)


def type_is_monitor_related(_type):
    if(_type == request_utils.MONITOR or _type == request_utils.MONITOR_RESPOND or _type == request_utils.CHANGE):
        return True
    return False


def calculate_avg_mem_use(_ev, _syst):
    for _service in _syst.services:
        for _theagent in _service.agents:
            _theagent
            
            
def calculate_avg_queue_use(_ev, _syst):
    for _service in _syst.services:
        for _theagent in _service.agents:
            _theagent