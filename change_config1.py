import template_utils
import logging as lg
import argparse
import numpy as np

def change_trigger_config_auto(args : argparse.Namespace):
    trigger_config = template_utils.parse_trigger()
    agent_configs = template_utils.parse_agent_config()
    # print(trigger_config)
    for i in range(len(trigger_config)):
        trigger_config[i][0] = args.default_load
        trigger_config[i][4] = args.spike_load
    new_trigger = ""
    for i in range(len(trigger_config)):
        for j in range(4):
            new_trigger = new_trigger + str(trigger_config[i][j])+":"
        new_trigger = new_trigger + str(trigger_config[i][4]) + "\n"
    # print(new_trigger)
    
    with  open("./Configs/trigger_config.txt", "w") as f:
        f.write("")
    with open("./Configs/trigger_config.txt", "a") as f:
        f.write(new_trigger)
    
def change_agent_config(_mode_to_rep):
    ###read the content in agent config and reqrite it with mode change to _mode tp rep
    ##input: "CONST" / "MUL" / "BUCK"
    ##
    result = []
    with  open("./Configs/agents_config.txt", "r") as f:
        for line in f:
            temp = line.split(":")
            temp[-1] = _mode_to_rep
            tempres = ":".join(temp)
            result.append (tempres)
    
    print(result)
    with  open("./Configs/agents_config.txt", "w") as f:
        f.write("")
    
    with open("./Configs/agents_config.txt", "a") as f:
        
        f.write("\n".join(result))

if __name__ == "__main__":
    log_file = open("log.txt", 'w')
    
    lg.basicConfig(filename="log.txt", format = "%(filename)s:%(lineno)d %(message)s", level = lg.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--default_load',
                        type=int,
                        required=True,
                        help='numbe of request per timeslot')
    parser.add_argument('--spike_load',
                        type=int,
                        required=True,
                        help='numbe of request per timeslot')
    args = parser.parse_args()
    
    change_trigger_config_auto(args)
    
    log_file.close()
    #plot_results(args.avg_len)
    