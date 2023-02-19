'''
Node class for the graph.

@author: Xiangyun Rao
'''
import numpy as np



class Node():
    def __init__(self, id:int, u:float):
        '''
        Constructor for the Node class.
        @param id: the id of the node
        @param u: the effiency of the node
        '''
        self.id = id
        self.u = u
        self.t = 0
        self.current_state = 1/u
        self.time = 0
        self.neighbor = []    
