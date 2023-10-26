# Ifc2vec


*Ifc2vec* is a simple yet effective technique to convert the Industry Foundation Classes (IFC) hierarchical schema into a vector representation from our [Semantic-aware quality assessment of building elements using graph neural networks (BIM-GNN)](https://www.sciencedirect.com/science/article/pii/S092658052300314X) paper. This vector representation is an alternative to the one-hot encoding of IfcClasses and can be used to perform similarity search, clustering, and other machine learning tasks. The key in the *ifc2vec* dictionary is the IfcCLass, and the value is the vector representation.

<p align="center">
  <img width="800" src="img/ifc2vec.png">
</p>

Fig 1. A sub-tree in *ancestors tree* and its one-hot and *ifc2vec* encodings. In *ifc2vec*, similar types are less distant than dissimilar ones ($\vec{e}.\vec{f} > \vec{e}.\vec{h}$), while in one-hot encoding, they are equally distant ($\vec{e}.\vec{f} = \vec{e}.\vec{h}$).

## Overview

Most learning algorithms require numeric input variables, so categorical features must be transformed to numeric during pre-processing. One-hot encoding is a typical method to convert categorical features to one-hot vectors. This technique assumes that the feature categories are independent. However, the IFC schema follows a hierarchical class structure where each class has associations with others. Moreover, some IFC classes may be ambiguous if the context is overlooked. For instance, *IfcCovering* may be related to a ceiling, flooring, molding, or cladding. Therefore, the one-hot encoding of the interrelated classes in the IFC data model may be a naïve approach.

We introduce *ifc2vec*, a simple yet effective method to convert an IFC EXPRESS schema (e.g., IFC2X3) into a look-up dictionary, $ifc2vec: IfcClass \to {\mathbb{R}}^n $. Our *ifc2vec* is useful for encoding element types considering their semantic relationships in learning-based or data-mining tasks. We extract the hierarchical inheritance relationships between the IFC classes and represent them as a tree that we call *ancestors tree*. This is done using ifcOWL [[1](http://dx.doi.org/10.1016/j.autcon.2015.12.003)], i.e., a Web Ontology Language (OWL) representation of the IFC schema. The root of the tree is the highest level in the IFC schema that one cares about. The children are classes that inherit from the parent class. For quality assessment purposes, *IfcProduct* is opted to be the root. By mapping a meaningful portion of the IFC to a tree, IFC classes can be represented as binary vectors indicating the path from the root to its node in the tree. For instance, sub-classes of *IfcWall*, siblings *IfcWallElementedCase* and *IfcWallStandardCase*, have closer vector embeddings in *ifc2vec* than dissimilar ones such as *IfcWallElementedCase* and *IfcDistributionPort* (Fig 1).

## Citation

If you use this code, please cite the following paper:

```
@article{KAYHANI2023BIMGNN,
title = {Semantic-aware quality assessment of building elements using graph neural networks},
journal = {Automation in Construction},
volume = {155},
pages = {105054},
year = {2023},
issn = {0926-5805},
doi = {https://doi.org/10.1016/j.autcon.2023.105054},
author = {Navid Kayhani and Brenda McCabe and Bharath Sankaran},
```

## Usage
1. Clone the repository to your local machine using `git clone https://github.com/navidk381/ifc2vec.git`.
2. Install the dependencies listed in the `requirements.txt` file. See the instructions below.

    a.  Using `pip` and `virtualenv`

    To install the dependencies listed in the `requirements.txt` file, follow these steps:

    1. Open a terminal window and navigate to the root directory of your project.
    2. Create a new virtual environment by running `python -m venv env` in the terminal. This will create a new directory called `env` in your project directory.
    3. Activate the virtual environment by running `source env/bin/activate` on macOS/Linux or `.\env\Scripts\activate` on Windows.
    4. Install the dependencies by running `pip install -r requirements.txt` in the terminal. This will install all the packages listed in the `requirements.txt` file.
    5. You can now run your project with the installed dependencies.

    Note: If you add or remove packages from the `requirements.txt` file, you will need to re-run `pip install -r requirements.txt` to update the installed packages.

    b. Using `Conda`

    Alternatively, you can use Conda to create a new environment and install the dependencies. Here are the steps:

    1. Open a terminal window and navigate to the root directory of your project.
    2. Create a new Conda environment by running `conda create --name myenv` in the terminal. This will create a new environment called `myenv`.
    3. Activate the Conda environment by running `conda activate myenv` in the terminal.
    4. Install the dependencies by running `conda install --file requirements.txt` in the terminal. This will install all the packages listed in the `requirements.txt` file.
    5. You can now run your project with the installed dependencies.

    Note: If you add or remove packages from the `requirements.txt` file, you will need to re-run `conda install --file requirements.txt` to update the installed packages.


3. Import the necessary functions from the ifc2vec.py file into your Python script.
4. Call the ifc2vec function with a dictionary of IFC schema hierarchy as an argument.
5. The function will return a dictionary of IFC schema hierarchy in vector representation.

```python
from ifc2vec import ifc2vec
from ancestors_tree import build_ancestors_tree_dictionary

# Build the IFC schema hierarchy dictionary
ifc_ancestors_tree = build_ancestors_tree_dictionary()

# Convert the IFC schema hierarchy to a vector representation
ifc2vec_dict = ifc2vec(ifc_ancestors_tree)

# Use the resulting dictionary for further analysis or processing
```
or a more advanced example, which is the code used to generate the ifc2vec dictionary for IFC2X3 schema with IfcProduct as the root:
```python
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os
from ancestors_tree import build_ancestors_tree_dictionary
from utils import get_config
import pickle

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
```

You can use the already processed **Ifc2vec** dictionaries for IFC2X3 schema with IfcProduct as the root in `.pkl` and `.pth` formats. The `.pkl` file is a Python dictionary, and the `.pth` file is a PyTorch tensor. The **ifc2vec** dictionary can be used for representing IFC classes as vectors considering their hierarchical relationships. 

The `.pth` file can be loaded as follows:
```python
import torch
ifc2vec_dict = torch.load('ifc2vec_dict.pth')
```

The `.pkl` file can be loaded as follows:
```python
import pickle
with open('ifc2vec_dict.pkl', 'rb') as f:
    ifc2vec_dict = pickle.load(f)
```
