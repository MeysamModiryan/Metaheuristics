import pandas as pd
from math import dist

def dataset_info():
    '''this function reads the information about all datas
       and returns informations as a pandas table BKS'''
    
    #readin excel format file with pandas
    BKS =  pd.read_excel('BKS.xlsx', sheet_name='BKS')
    
    #rename the features
    BKS.rename(columns={'Ins':'file_name', 'n':'Nom_of_node', 'K':'K_min', 'Q':'veh_cap'}, inplace=True)
    
    # Add '.txt' to file_name values
    for i in range(len(BKS['file_name'])):
        BKS.loc[i,'file_name'] = BKS.loc[i,'file_name']+str('.txt')
    return BKS

def get_files(info):
    ''' This function reads all text files and pass them to a dictionary'''
    
    # Reading each file.txt as a table an save all them in a dictionary
    File_Name_dic = {}
    rows= info.index.tolist()
    for row in rows:
        File_Name_dic['data'+str(row)] = pd.read_table(info.loc[row, 'file_name'])
    return rows, File_Name_dic


def get_table(BKS, File_Name_dic,rows):
    ''' Extracts tables from text files and saves them as dictionaries'''
    
    Locations={}
    Demands = {}
    
    # defining some parameters for slicing 
    L_N = 6+BKS['Nom_of_node']
    D_N_L = L_N+2
    D_N_U = D_N_L + BKS['Nom_of_node']
    
    # reading cotumers' location and costumers' demand from each file
    for row in rows:
        Locations['loc'+str(row)] = File_Name_dic['data'+str(row)].loc[6:L_N[row]]
        col2 = str(Locations['loc'+str(row)].columns[1])
        Locations['loc'+str(row)].rename(columns={'NAME : ':'ind',col2:'x','Unnamed: 2':'y'}, inplace=True)
        Locations['loc'+str(row)].set_index('ind', inplace=True)
    
        Demands['dem'+str(row)] = File_Name_dic['data'+str(row)].loc[D_N_L[row]:D_N_U[row]]
        Demands['dem'+str(row)].rename(columns={'NAME : ':'ind',col2:'d'}, inplace=True)
        Demands['dem'+str(row)].set_index('ind', inplace=True)
        Demands['dem'+str(row)].drop('Unnamed: 2',axis=1, inplace=True)
    return Locations, Demands

def get_data_information(Instance):
    instance = Instance-1
    data_information = dataset_info()
    rows, Files_name = get_files(data_information)
    Locations, Demands = get_table(data_information, Files_name, rows)
    df = Locations['loc'+str(instance)].astype(float)
    num_of_customer = data_information.loc[instance,'Nom_of_node']
    customer_list = [i for i in range(1,num_of_customer+1 )]
    all_nodes = [i for i in range(num_of_customer+1)]
    coords = [(i,j) for i in all_nodes for j in all_nodes if i!=j]
    distance = {(i,j): round(dist((df['x'][i],df['y'][i]), (df['x'][j],df['y'][j]))) for i,j in coords}
    f_star = data_information.loc[instance, 'UB']
    demand = Demands['dem'+str(instance)]['d'].astype(float)           
    capacity = data_information.loc[instance,'veh_cap']
    K_min = data_information.loc[instance,'K_min']

    parameters = {'data_information':data_information,
                  'location':df,
                  'distance':distance,
                  'num_of_customer':num_of_customer,
                  'customer_list': customer_list,
                  'all_nodes': all_nodes,
                  'coords': coords,
                  'distance': distance,
                  'f_star':f_star,
                  'demand': demand,
                  'capacity': capacity,
                  'K_min': K_min}
    return parameters