import random
def neighborhood(N):
    ''' gets current route and improves it'''
#     this funcion gets current path or route and passes clients to a list by allocation priority.
#     gets a client randomly and chooses it as the first client that will be visited.  
#     after that checks the list and assigns the nearest client  to the current route
#     actually, this function reorders clients by choosing a random client
    
    r = random.sample(N, 2)
    i1 = N.index(r[0])
    i2 = N.index(r[1])
    if i2<i1:
        t  = i1
        i1 = i2
        i2 = t
    chance = np.random.uniform()
    if chance<0.7:
        N[i1-1],N[i2-1] = N[i2-1],N[i1-1]
    else:
        N.remove(max(r))
        N.insert(min(r), max(r))
    return N

import numpy as np
from Functions import*
from Initial_Solution import*
from DataInfo import*
import time
import matplotlib.pyplot as plt

def N_neighborhood(N,param, dis):
    ''' gets current route and improves it'''
#     this funcion gets current path or route and passes clients to a list by allocation priority.
#     gets a client randomly and chooses it as the first client that will be visited.  
#     after that checks the list and assigns the nearest client  to the current route
#     actually, this function reorders clients by choosing a random client
    r = random.sample(N, 1)[0]
    m = np.argmin(dis[r])
    
    chance = np.random.uniform()
    if chance<0.5:
        if r>m:
            i1 = m
            i2 = r
        else:
            i1 = r
            i2 = m
        N[i1-1],N[i2-1] = N[i2-1],N[i1-1]
    else:
        N.remove(m)
        N.insert(r, m)
    return N

def SA_Model(NUMBER_OF_ITERATIONS = 5,
             initiaTemperature=2000,
             coolingRate=0.99, 
             finalTemperatur=0.1, 
             Instance=1, 
             Neighbor_Method="NN",
             Initial_Method = "Random"):
    """
    describe your model
    """
    #Initial variables
    GLOBAL_OPT     = np.inf                     #To save best objective function that found
    Current_loss   = np.inf                     #To save objective function in each iteration
    G_best_Route   = {}                         #To save the route corresponding to GLOBAL_OPT                
    Current_Route  = {}                         #To save the route corresponding to G_best_Route  
    iter_Number    = 0
    Loss           = []
    
    parameter = get_data_information(Instance)
    dis = distance_array(parameter)
    if Initial_Method == "Random":
        initial_solution = Random_initial_solution(parameter)
    elif Initial_Method == "Nearest_Neighbor":
        initial_solution = Nearest_Neighbor_Initial_solution(parameter)
    else: print("You have to choose initial method correctly, Please pich it from the list [Random, Nearest_Neighbor]")
    active, Y = active_graph(initial_solution, parameter['coords'])
    loss = comput_cost(parameter['distance'], active)
   
    Current_loss = loss
    Current_Route = initial_solution
    Loss.append(loss)
    
    if Current_loss < GLOBAL_OPT:
        GLOBAL_OPT = Current_loss
        G_best_Route = Current_Route 
    
    temperature=initiaTemperature 
    tic = time.time()
    
    while temperature>finalTemperatur:
                
        if iter_Number % 100 == 0:
            print('loss is:', loss,'<=====> bestsofar is: ', GLOBAL_OPT, ' temprature is:', temperature)
        for i in range(NUMBER_OF_ITERATIONS):
            X = decode(Current_Route)
            if Neighbor_Method == "NN":
                Route = N_neighborhood(X,parameter, dis)
            elif Neighbor_Method == "Random":
                Route = neighborhood(X)
            elif Neighbor_Method == "Hybrid":
                chance = np.random.uniform()
                if chance < 0.5:
                    Route = N_neighborhood(X,parameter, dis)
                else:
                    Route = neighborhood(X)
            else: print('You have to choose neighbor method correctly.')
                
            Route = get_route(Route, parameter)
            active, Y = active_graph(Current_Route, parameter['coords'])
            loss = comput_cost(parameter['distance'], active)
            if loss < Current_loss:
                Current_loss = loss
                Current_Route = Route
            else:
                delta_loss = (Current_loss - loss)
                r = np.random.uniform()
                if r < np.exp(delta_loss/temperature):
                    Current_loss = loss
                    Current_Route = Route

                    
        if Current_loss < GLOBAL_OPT:
            GLOBAL_OPT = Current_loss
            G_best_Route = Current_Route
        Loss.append(GLOBAL_OPT)
        temperature = coolingRate * temperature
        iter_Number +=1
    toc = time.time()
    CPU_T = (toc - tic)/60
    print(iter_Number)
    plt.plot(Loss)
    return GLOBAL_OPT, G_best_Route, CPU_T
