'''
This is the distributed algorithm for the multi-agent allocation problem.

@author: Xiangyun Rao
'''
import numpy as np
import time
from node import Node

def split_integer(m, n):
    '''
    A function to split an integer into n parts.

    @param m: the integer to be split
    @param n: the number of parts

    @return: the list of parts
    '''
    assert n > 0
    quotient = int(m / n)
    remainder = m % n
    if remainder > 0:
        return [quotient] * (n - remainder) + [quotient + 1] * remainder
    if remainder < 0:
        return [quotient - 1] * -remainder + [quotient] * (n + remainder)
    return [quotient] * n

def set_neighbors(node:Node, nei:list):
    '''
    A function to set the neighbors of a node.

    @param node: the node to set the neighbors
    @param nei: the list of neighbors

    @return: the nodes with neighbors
    '''
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if nei[i][j] > 0:
                nodes[i].neighbor.append(j + 1)
    return nodes


def initialize(nodes:list, tasks:int, nei:list):
    '''
    Initialize the nodes.
    @param nodes: the list of nodes
    @param tasks: the number of tasks

    @return: the initialized nodes
    '''
    current_best = 0 # The current best time
    initialize_allocation = split_integer(tasks, len(nodes))
    nodes = set_neighbors(nodes, nei)
    for i in range(len(nodes)):
        # 随机领取整数个任务，但是加起来要等于tasks
        nodes[i].t = initialize_allocation[i]
        nodes[i].time = nodes[i].t / nodes[i].u
        nodes[i].current_state = nodes[i].time + 1 / nodes[i].u
        # sort the neighbors
        nodes[i].neighbor.sort()
        print(nodes[i].neighbor)
        if nodes[i].time > current_best:
            current_best = nodes[i].time
    return nodes, current_best


def choose_nodes(n:int, nodes:list):
    '''
    A function to choose the nodes to communicate.
    
    @param n: the number of nodes

    @return: the node to communicate
    '''
    return nodes[np.random.randint(1, n+1) - 1]

def distributed(nodes:list, tasks:int, nei:list):
    nodes, current_best_time = initialize(nodes, tasks, nei)
    rest_tasks = tasks
    # sort the nodes according to the current state, from large to small
    tools = nodes
    tools.sort(key=lambda x: x.time, reverse=True)
    start_time = time.time()
    flag = False
    # main loop
    while True:
        current_node = choose_nodes(len(nodes), nodes)
        potential_neighbors = []
        used_to_be = []
        while True:
            for neibo in current_node.neighbor:
                if nodes[neibo - 1].current_state < current_node.time:
                    potential_neighbors.append(nodes[neibo - 1])
            if len(potential_neighbors) == 0:
                # No neighbor can help, so the current node will do the task
                used_to_be = []
                rest_tasks -= 1
                tools.sort(key=lambda x: x.time, reverse=True)
                current_best_time = tools[0].time
                break
            else:
                # Choose the neighbor with the smallest current state
                potential_neighbors.sort(key=lambda x: x.current_state)
                neighbor = potential_neighbors[0]
                if neighbor.id in used_to_be:
                    # The neighbor has been used to be the current node
                    rest_tasks -= 1
                    used_to_be = []
                    tools.sort(key=lambda x: x.time, reverse=True)
                    current_best_time = tools[0].time
                    break
                used_to_be.append(current_node.id)
                current_node.t -= 1
                current_node.time = current_node.t / current_node.u
                current_node.current_state = current_node.time - 1 / current_node.u
                neighbor.t += 1
                neighbor.time = neighbor.t / neighbor.u
                neighbor.current_state = neighbor.time + 1 / neighbor.u
                tools.sort(key=lambda x: x.time, reverse=True)
                current_best_time = tools[0].time
                current_node = neighbor
                current_allocations = [node.t for node in nodes]
                print('The current best time is: ', current_best_time, 'The rest tasks are: ', rest_tasks, 
                'current_time is:', time.time() - start_time, 'current allocation:', current_allocations,
                flush=True, end='\r')
        if rest_tasks == 0:
            break
        # 显示当前的最佳时间，不断更新
        
    print('The best time is: ', current_best_time)
    print('The allocation is: ', [node.t for node in nodes])
    print('The u is: ', [node.u for node in nodes])


        
        
        


if __name__ == '__main__':
        # The parameters
    N = 5 # The number of agents
    M = 100000 # The number of tasks
    mode = 2 # The random mode, 0 for the integer mode, 1 for the real number mode,3 for self-defined
    A = [[0, 9/10, 0, 0, 1],    
     [1, 0, 8/9, 4/3, 0],
     [0, 1, 0 ,1, 0],
     [0, 1, 2/3, 0, 1],
     [10/11, 0, 0, 12/11,0]]
    if mode ==  0:
        u = np.random.uniform(2, 10, N) # The efficiency of the agents
    elif mode == 1:
        u = np.random.randint(2, 10, N)
    elif mode == 2:
        u = np.array([1000, 900, 800, 1200, 1100])
    print('The efficiency of the agents are: ')
    print(u)
    # The initialization
    nodes = []
    for i in range(1, N + 1):
        nodes.append(Node(i, u[i - 1]))
    distributed(nodes, M, A)
