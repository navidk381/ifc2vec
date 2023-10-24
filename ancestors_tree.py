from utils import get_config, read_ifc_owl, build_ifc_network, ifc_network_to_tree

def build_descendants_tree(ifc_owl_path = None, parent_class = None, show_tree = True):
    '''
    Build the descendants tree from the parent class and the ifc owl file. Each node in the tree is an ifc class.

    Args:
        ifc_owl_path: path to the ifc owl file
        parent_class: parent class of the ifc network
        show_tree: whether to show the tree
    
    Returns:
        descendants_tree: descendants tree where root is the parent class and leaves are the descendants

    Example:

    IfcProduct
    ├── IfcAnnotation
    ├── IfcElement
    │   ├── IfcBuildingElement
    │   │   ├── IfcBeam
    │   │   │   └── IfcBeamStandardCase
    │   │   ├── IfcBuildingElementProxy
    │   │   ├── IfcChimney
    │   │   ├── IfcColumn
    │   │   │   └── IfcColumnStandardCase
    │   │   ├── IfcCovering
    │   │   ├── IfcCurtainWall
    │   │   ├── IfcDoor
    │   │   │   └── IfcDoorStandardCase
    │   │   ├── IfcFooting
    │   │   ├── IfcMember
    │   │   │   └── IfcMemberStandardCase
    │   │   ├── IfcPile
    │   │   ├── IfcPlate
    │   │   │   └── IfcPlateStandardCase
    │   │   ├── IfcRailing
    │   │   ├── IfcRamp
    │   │   ├── IfcRampFlight
    │   │   ├── IfcRoof
    │   │   ├── IfcShadingDevice
    ...
            │   └── IfcStructuralCurveMemberVarying
            └── IfcStructuralSurfaceMember
                └── IfcStructuralSurfaceMemberVarying


        
    '''
    if ifc_owl_path is None:
        print('[INFO] ifc owl path not provided, using the default path')
        ifc_owl_path = get_config('ifc_owl_path')

    ifc_graph, result = read_ifc_owl(ifc_owl_path)
    
    if parent_class is None:
        print('[INFO] parent class not provided, using the default parent class')
        parent_class = get_config('parent_class')

    ifcnetwork = build_ifc_network(parent_class, ifc_graph)

    descendants_tree = ifc_network_to_tree(ifcnetwork, parent_class, show_tree)

    return descendants_tree



def build_ancestors_tree_dictionary(ifc_owl_path = None, parent_class = None, show_tree = True):
    '''
    Build the ancestors tree based the parent class and the ifc owl file as a dictionary.
    Each key represents an ifc class and the value is a list of its ancestors (parents).

    Args:
        ifc_owl_path: path to the ifc owl file
        parent_class: parent class of the ifc network
        show_tree: whether to show the descendants_tree 
    
    Returns:
        descendants_tree_dictionary: the dictionart of parents (ancestors)
    '''
    tree = build_descendants_tree(ifc_owl_path, parent_class, show_tree)    

    t_id = tree.identifier
    parents = {}
    for _, node in tree.nodes.items():
        parent_names = []
        parent_name = node.predecessor(t_id)
        while parent_name:
            parent_names.append(parent_name)
            parent_node = tree[parent_name]
            parent_name = parent_node.predecessor(t_id)
        parents[node.identifier] = parent_names
    
    return parents
    


