import matplotlib.pyplot as plt
import numpy as np
import argparse
import logging as lg

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
    change_agent_config("MUL")