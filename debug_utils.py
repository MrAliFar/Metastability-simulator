import logging as lg

def print_unwrapped(instances):
    for inst in instances:
        lg.info(vars(inst))

def print_list_unwrapped(lists):
    for lst in lists:
        #lg.info("Next")
        for inst in [lst]:
            lg.info(vars(inst))