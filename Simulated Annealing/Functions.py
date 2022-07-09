import pandas as pd
import numpy as np
from random import sample
from math import degrees, atan2, sqrt


def coordinates(df, BKS):
    '''return coordinates all points'''
    depo = df.iloc[0,:]
    x_d, y_d = depo[0], depo[1]
    x_c, y_c = df['x'][1:], df['y'][1:]
    return x_d, y_d, x_c, y_c

def comput_cost(D, active):
    '''to compute objective or loss function'''
    Total_cost = 0
    for i,j in active:
        Total_cost +=D[i,j]
    return Total_cost

def active_graph(Rout, cr):
    ''' Gets route and and return active arcs in netwark'''
    
    Y = {(i,j):0 for i,j in cr}  #Binary variable is 1 if vehicle visits client j after visiting client i 
    for key in Rout.keys():
        for i in range(len(Rout[key])):
            if Rout[key][i] == Rout[key][-1]:
                j=0
            else: j = Rout[key][i+1]
            Y[Rout[key][i], j]=1
    active_arcs = [i for i in cr if Y[i]>0]
    return active_arcs, Y

def get_route(client_priority,param):
    n   = param['num_of_customer']
    d   = param['demand']
    Q   = param['capacity']
    cp =list(map(int,client_priority))
    Initial_Route = {}   
    is_visited = [False for i in range(n)]
    j=0
    # for each customer checks the capacity feasibility of a route and assigns it
    while sum(is_visited)!=n:
        u = 0
        Initial_Route[j] = [0]
        for i in cp :
            if is_visited[i-1]==False:
                if u+d[i] <= Q:
                    Initial_Route[j].append(i)
                    is_visited[i-1]=True
                    u = u+d[i]
        j+=1
    return Initial_Route

def Clients_Angles(data_par):
    df = data_par['location']
    d_info = data_par['data_information']
    x_d, y_d, x_c, y_c = coordinates(df, d_info)
    angles =[]
    for i in range(len(x_c)):
        angles.append(calculateDepotAngle(x_c[i],y_c[i],x_d,y_d))
    return angles

def calculateDepotAngle(x,y,depot_x,depot_y):
    angle = degrees(atan2(y - depot_y, x - depot_x))
    bearing = (90 - angle) % 360
    return bearing

def Creating_Particle(angles,Co_list):
    particle = []
    angles = np.asanyarray(angles)
    k = []
    K = 0
    k.append(K)
    ANGLE=[]

    while K in k :
        K = sample(list(angles),1)[0]
    k.append(K)
    Angle = angles-K
    for j in list(Angle):
        if j<0:
            j+=360
        ANGLE.append(j)
    a = [float(x) for _,x in sorted(zip(ANGLE,Co_list))]
    a = np.asanyarray(a)
    b = np.random.uniform(low=1, high=Dimention_size, size=a.size)
    temp = np.stack((a, b), axis=1)
    particle.append(temp)
    particle = np.asanyarray(particles)
    return particle

def decode(route):
    merge=[0]
    for i in route.values():
            merge+=i
    my_list = np.asarray(merge)
    N =list(dict.fromkeys(my_list))
    N.remove(0)
    return N