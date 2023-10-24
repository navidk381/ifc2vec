# read yaml file
import yaml
import os
import requests.auth
import rdflib
from treelib import Node, Tree


def get_config(name, config_path = './config/defaults.yaml'):
    '''
    Read yaml file and return the value of the key 'name'

    Args:
        name: key name
        config_path: path to the yaml file
    
    Returns:
        config[name]: value of the key 'name'
    '''
    assert os.path.exists(config_path), 'Config file not found: {}'.format(config_path)
    with open(config_path) as file:
        # read yaml file
        config = yaml.load(file, Loader=yaml.FullLoader)

        # read ifc owl file in the config file
        assert name in config, f'{name} not found in {config_path}'
        return config[name]


def read_ifc_owl(file_path):
    '''
    Read ifc owl file and return the graph

    Args:
        file_path: path to the ifc owl file

    Returns:
        ifc_graph, result: graph of the ifc owl file and the result of the parsing
    '''

    print('[INFO] ifc owl path: {}'.format(file_path))
    assert os.path.exists(file_path), 'File not found: {}'.format(file_path)
    print('[INFO] ifc owl file found')
    
    # reading the file
    ifc_graph = rdflib.Graph()
    result = ifc_graph.parse(file_path, format='ttl')
    print('[INFO] ifc owl file parsed')
    return ifc_graph, result
    

def build_ifc_network(parent_class, ifc_graph):
    '''
    Build the ifc network from the parent class

    Args:
        parent_class: parent class of the ifc network
        ifc_graph: graph of the ifc owl file
    
    Returns:
        ifcnetwork: ifc network
    '''
    ifcnetwork = {}
    queue=[parent_class]

    while len(queue)!=0:
        
        ifcclass=queue[0]
        ifcnetwork[ifcclass]=[]
        
        query = 'SELECT * WHERE {?s rdfs:subClassOf ifc:'+ifcclass+'.}'
        query_result = ifc_graph.query(query)
        
        if len(query_result)>0:
            for subclass in query_result:
                queue.append(subclass[0].split(sep='#')[1])
                ifcnetwork[ifcclass].append(subclass[0].split(sep='#')[1])
        
        queue.remove(ifcclass)
    return ifcnetwork



def ifc_network_to_tree(ifcnetwork, parent_class, show_tree=True):
    '''
    Convert ifc network to tree structure

    Args:
        ifcnetwork: ifc network
        parent_class: parent class of the ifc network
        show_tree: show the tree structure of the ifc network
    
    Returns:
        tree: tree structure of the ifc network
    '''

    tree = Tree()
    tree.create_node(parent_class,parent_class, parent=None)
    for key, value in ifcnetwork.items():
        for v in value:
            tree.create_node(v, v, parent=key)
    if show_tree:
        tree.show(stdout=False) 
    return tree 


# def are_files_equal(pth_file, npy_file):
#     import torch
#     import numpy as np
#     # Load data from the .pth file
#     try:
#         pth_data = torch.load(pth_file)
#     except Exception as e:
#         print(f"Error loading data from {pth_file}: {e}")
#         return False

#     # Load data from the .npy file
#     try:
#         npy_data = np.load(npy_file, allow_pickle=True)
#     except Exception as e:
#         print(f"Error loading data from {npy_file}: {e}")
#         return False

#     print((pth_data))
#     print((npy_data))

#     # Check if the shapes and data are the same
#     for k, v in pth_data.items():
#         if not np.array_equal(v, npy_data[k]):
#             print(k)
#             print("The contents of the .pth and .pkl files are the same.")
#             return True
#     else:
#         print("The contents of the .pth and .pkl files are not the same.")
#         return False

# # Example usage
# pth_file = "ifc2vec_IFC2x3.pth"
# npy_file = "ifc2vec_IFC2x3.pkl"

# are_files_equal(pth_file, npy_file)