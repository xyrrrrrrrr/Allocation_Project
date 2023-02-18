'''
This is the centralized algorithm for the multi-agent allocation problem.

@autor: Xiangyun Rao
'''
import numpy as np
import time
from node import Node

# The centralized algorithm
def centralized_algorithm(nodes:list, tasks:int):
    '''
    The centralized algorithm for the multi-agent allocation problem.
    @param nodes: the list of nodes
    @param tasks: the number of tasks

    @return: the best allocation and the total time
    '''
    start = time.time()
    # loop for the tasks
    for _ in range(tasks):
        # sort the nodes according to the current state, from large to small
        nodes.sort(key=lambda x: x.current_state)
        # allocate the task to the node with the smallest current state
        nodes[0].t += 1
        # update the current state and time of node
        nodes[0].current_state += 1 / nodes[0].u
        nodes[0].time += 1 / nodes[0].u
    end = time.time()
    print('Algorithm time: ', end-start)
    # return the best allocation and the total time
    total_time = nodes[0].time
    # sort the nodes according to the id
    nodes.sort(key=lambda x: x.id)
    print('The best allocation is: ', [node.t for node in nodes])
    print('The total time is: ', total_time)

    return nodes, total_time

if __name__ == '__main__':
    # The parameters
    N = 4 # The number of agents
    M = 10 # The number of tasks
    mode = 1 # The random mode, 0 for the integer mode, 1 for the real number mode
    if mode ==  0:
        u = np.random.uniform(2, 10, N) # The efficiency of the agents
    else:
        u = np.random.randint(2, 10, N)
    print('The efficiency of the agents are: ')
    print(u)
    # The initialization
    nodes = []
    for i in range(N):
        nodes.append(Node(i, u[i]))

    centralized_algorithm(nodes, M)
    


