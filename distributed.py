'''
This is the distributed algorithm for the multi-agent allocation problem.

@author: Xiangyun Rao
'''
import numpy as np
import time
from node import Node

def initialize(nodes:list, tasks:int):
    '''
    Initialize the nodes.
    @param nodes: the list of nodes
    @param tasks: the number of tasks

    @return: the initialized nodes
    '''
    current_best = 0 # The current best time
    for i in range(len(nodes)):
        # 随机领取整数个任务，但是加起来要等于tasks
        if i == len(nodes) - 1:
            nodes[i].t = tasks
        else:
            nodes[i].t = np.random.randint(0, tasks)
            tasks -= nodes[i].t
        nodes[i].time = nodes[i].t / nodes[i].u
        if nodes[i].time > current_best:
            current_best = nodes[i].time
    return nodes, current_best


def distributed(nodes:list, tasks:int):
    c_f = 100 # The communication frequency
    nodes, current_best_time = initialize(nodes, tasks)

    while True:
        


