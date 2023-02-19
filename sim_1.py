'''
This is a python version of the sim_1.m file whose author is Jialun Huang.

@author: Xiangyun Rao
'''
import numpy as np
import time
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # Parameters
    N = 5 # number of nodes
    color = 'brkm' # color for each node
    A=[[0, 9/10, 0, 0, 1],    
     [1, 0, 8/9, 4/3, 0],
     [0, 1, 0 ,1, 0],
     [0, 1, 2/3, 0, 1],
     [10/11, 0, 0, 12/11,0]]
    A = np.array(A)
    d = np.zeros(N)
    for i in range(N):
        d[i] = 0
        for j in range(N):
            d[i] = d[i] + A[i][j]
    gam = 0.25;
    D = np.diag(d.T)
    # print(D)
    L = D - A
    u1=1000
    u2=900
    u3=800
    u4=1200
    u5=1100
    u = np.array([u1, u2, u3, u4, u5])
    U = np.diag(u)
    L_e = np.dot(np.dot(U, L), np.linalg.inv(U))
    I = np.eye(N)
    P_e = I - gam * L_e
    # print(P_e)
    n = 3;
    # initialize
    x = np.ones((N, 24))
    # print(x[1,:].size)
    # input()
    y = np.zeros((N, 24))
    z = np.zeros((N, 24))
    x = x * 20000
    z[:, 0] = x[:, 0] - y[:, 0]
    for k in range(n):
        for i in range(N):
            y[i][k+1] = y[i][k] + u[i]
            z[i][k+1] = x[i][k+1] - y[i][k+1]

    # simulation
    temp = 0
    flag = 0
    for k in range(n, 23):
        # first allocate tasks dynamically
        if temp < N:
            x[:, k+1] = np.sum(P_e * x[:, k], axis = 1)
            # 四舍五入取整
            x[:, k+1] = np.round(x[:, k+1])
            for i in range(N):
                if x[i, k+1] - x[i, k] < gam * u[i]:
                    temp = temp + 1
            temp = 0
        else:
            x[:, k+1] = x[:, k]
        y[:, k+1] = y[:, k] + u
        for i in range(N):
            z[i ,k+1] = x[i, k+1] - y[i, k+1];
            if z[i, k+1] < 0:
                z[i, k+1] = 0
                flag += 1
        if np.sum(z[:, k]) == 0:
            print('All images are finished at day', k+1) 
            print('Best allocation is: ', x[:, k])
    
    fig_1 = plt.figure()
    t = range(0, x[1,:].size)
    tools = []
    for i in range(N-1):
        tools.append(plt.plot(t, x[i,:], marker='^', color = color[i], linewidth = 1.4))
    tools.append(plt.plot(t, x[N-1,:], marker = '^', color = [0,0.4,0], linewidth = 1.4, markersize = 4))
    plt.xlabel('day');
    plt.ylabel('Number of Total Images');
    l1 = plt.legend(tools, ['Group 1','Group 2','Group 3','Group 4','Group 5'], loc='upper left')
    # plt.legend('Group 1','Group 2','Group 3','Group 4','Group 5');
    # plt.show()

    fig_2 = plt.figure()
    t = range(0, z[1,:].size)
    tools = []
    for i in range(N-1):
        tools.append(plt.plot(t, z[i,:], marker='s', color = color[i], linewidth = 1.4))
    tools.append(plt.plot(t, z[N-1,:], marker = 's', color = [0,0.4,0], linewidth = 1.4, markersize = 4))
    plt.xlabel('day');
    plt.ylabel('Number of Unfinished Images');
    plt.legend(tools, ['Group 1','Group 2','Group 3','Group 4','Group 5'], loc='upper left')
    plt.show()