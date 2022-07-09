from random import shuffle,sample
import numpy as np
import math
from Functions import*

def Random_initial_solution(param):
    ''' gets parameters and distance and create a random feasible solution '''
    
    N = param['customer_list']
    shuffle(N)
    route = get_route(N, param)
    return route


def Nearest_Neighbor_Initial_solution(param): 

    n   = param['num_of_customer']
    d   = param['demand']
    dist= param['distance']
    Q   = param['capacity']

    H = [l for l in range(n+1)]
    coord_h = [(s,w) for s in H for w in H if s!=w]
    Y = {(m,n):dist[(m,n)] for m,n in coord_h}

    Initial_Rout={}
    all_checked = [False for c in range(1, n+1)]
    j = 0
    Initial_Rout[j] = [0]
    node_visited_init = [0]
    r = sample(H, 1)[0]
    Initial_Rout[j].append(r)
    node_visited_init.append(r)
    all_checked[r-1] = True
    while sum(all_checked)!= n:
        a = Initial_Rout[j][-1]
        my_list = {}
        for b in H:
            if b not in node_visited_init:
                if b!=a:
                    my_list[b]=Y[(a,b)]
        my_list_as = {k: v for k, v in sorted(my_list.items(), key=lambda item: item[1])}
        my_list_key = list(my_list_as.keys())
        my_list_value = list(my_list_as.values())
        index = 0
        node_ass = False
        rout_deman = [d[s] for s in Initial_Rout[j]]
        u = np.sum(rout_deman)
        while node_ass == False and index<=3:
            visit = my_list_key[index]
            if all_checked[visit-1]==False:
                if u+d[visit] <= Q:
                    Initial_Rout[j].append(visit)
                    all_checked[visit-1]=True
                    u = u+d[visit]
                    a = visit
                    node_visited_init.append(visit)
                    node_ass = True
                    break
            index+=1
            if index >=len(my_list_key):
                break
        node_not_visited = [e for e in H if e not in node_visited_init]
        node_not_vi_dem = [d[t] for t in node_not_visited]
        rout_deman = [d[w] for w in Initial_Rout[j]]
        slack = Q - np.sum(rout_deman)
        try:
            if slack < min(node_not_vi_dem) or index >=3:
                j+=1
                Initial_Rout[j] =[0]
                r = sample(node_not_visited, 1)[0]
                Initial_Rout[j].append(r)
                node_visited_init.append(r)
                all_checked[r-1] = True
        except: ValueError
    return Initial_Rout
