import numpy as np
from sklearn.preprocessing import LabelEncoder
import os
from ancestors_tree import build_ancestors_tree_dictionary
from utils import get_config
import pickle

def _one_hot_encoder(categorical_data):
    """
    One-hot encodes a categorical feature and returns the one-hot encoded array and the label encoder object.

    Args:
        categorical_data (list): list of categorical data
    
    Returns:
        numpy.ndarray: one-hot encoded array
        LabelEncoder: label encoder object
    """
    le = LabelEncoder()
    labels_int = le.fit_transform(categorical_data)
    
    num_samples = len(categorical_data)
    num_classes = len(le.classes_)
    
    labels_one_hot = np.zeros((num_samples, num_classes), dtype=np.float32)
    labels_one_hot[np.arange(num_samples), labels_int] = 1.0
    
    return labels_one_hot, le

def ifc2vec(ifc_ancestors_tree:dict) -> dict:
    """
    Convert IFC schema hierarchy (e.g., IfcElement and its children) to a vector representation

    Args:
        ifc_ancestors_tree (dict): dictionary of IFC schema hierarchy

    Returns:
        ifc2vec_dict: dictionary of IFC schema hierarchy in vector representation
    """
    one_hot, le = _one_hot_encoder(list(ifc_ancestors_tree.keys()))
    ifc2vec_dict = {}
    for ifc_entity, ancestors in ifc_ancestors_tree.items():
        # find the index of the ifc_entity and its ancestors
        ifc_entity_index = le.transform([ifc_entity])
        ancestors_index = le.transform(ancestors)

        # create a zero vector and set the index of the self and its ancestors to 1
        encoding = np.zeros_like(one_hot[0])
        encoding[ifc_entity_index] = 1
        if ancestors_index.size > 0:
            encoding[ancestors_index] = 1

        # add the encoding to the ifc2vec dictionary
        ifc2vec_dict[ifc_entity] = encoding

    return ifc2vec_dict


if __name__ == '__main__':
    # build the ifc ancestors tree
    ifc_ancestors_tree = build_ancestors_tree_dictionary()

    # get the deprecated ifc types for the IFC2x3 schema
    try:
        deprecated_ifc_types = get_config('DEPRECATED_IFC_TYPES', config_path='./config/deprecated_ifc_types.yaml')
    except Exception as e:
        print(e)
        deprecated_ifc_types = {}
        raise 
    
    try:
        ifc_ancestors_tree = ifc_ancestors_tree | deprecated_ifc_types
    except Exception as e:
        print(e)
        raise

    # convert the ifc ancestors tree to ifc2vec dictionary (vector representation)
    ifc2vec_dict = ifc2vec(ifc_ancestors_tree)


    # remove the deprecated ifc types from the ifc2vec dictionary

    #save the ifc2vec dictionary as pickle file
    if get_config('save_ifc2vec_dict'):
        path = get_config('ifc2vec_dict_path')
        # save the ifc2vec dictionary 
        with open(path, "wb") as pickle_file:
            pickle.dump(ifc2vec_dict, pickle_file)
    print('ifc2vec dictionary saved at: ', path)


