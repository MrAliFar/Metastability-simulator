import logging as lg

def print_unwrapped(instances):
    for inst in instances:
        lg.info(vars(inst))

def print_list_unwrapped(lists):
    for lst in lists:
        #lg.info("Next")
        for inst in [lst]:
            lg.info(vars(inst))

def print_queue(q):
    my_str = ""
    for elem in list(q.queue):
        my_str = my_str + " " + str(elem.syst_id)
    lg.info(f"{my_str}")
        