from node import Node
from tree import Tree
from typing import Dict, List, Union, TextIO


# Declaring my nodes dictionaries
nodes: Dict[str, Node] = {}
incompleteNodes: Dict[str, List[List[Union[str, int]]]] = {}

# Declaring my tree
tree: Tree = Tree()


# Sorter which put leaves first in the list
def leaves_first(value: str):
    return len(value.split(" "))


# A simple treatment on each node when running through the tree
def give_your_name(current_node: Node):
    print(current_node.name)


def creating_nodes_from_file(file: TextIO):

    lines: List[str] = file.readlines()

    lines.sort(key=leaves_first)

    for line in lines:

        # removing \n at the end of the line
        line: str = line[:-1]
        args: List[str] = line.split(" ")

        node_name: str = args[0]

        nodes[node_name] = Node(node_name, 0, [None] * len(args[1:]) if len(args) > 1 else None)

        if len(args) > 1:
            node_children_name: List[str] = args[1:]

            for idx, child in enumerate(node_children_name):

                # If the child have already been created
                if nodes.get(child):
                    nodes[child].increase_depth(nodes[node_name].depth)
                    nodes[node_name].children[idx] = nodes[child]

                # Else, we wait the end to complete the node
                else:

                    if incompleteNodes.get(node_name):
                        children: List[List[Union[str, int]]] = incompleteNodes[node_name]
                        children.append([child, idx])
                    else:
                        incompleteNodes[node_name] = [[child, idx]]


def update_incomplete_nodes():
    while len(incompleteNodes) > 0:

        node_name, children = incompleteNodes.popitem()

        # Check if all children have been created
        remaining_children_to_complete: List[List[Union[str, int]]] = []
        for couple in children:
            # A couple is the child name and its position in dad's children list
            child_name: str = couple[0]
            idx_child: int = couple[1]

            # If the child exists, just add it to the node children list
            if nodes.get(child_name):
                current_node: Node = nodes.get(node_name)
                children: List[Node] = nodes[node_name].children
                nodes.get(child_name).increase_depth(current_node.depth)
                children[idx_child] = nodes.get(child_name)

            # Else, update the list of missing nodes
            else:
                remaining_children_to_complete.append([child_name, idx_child])

        # If my node still needs to wait for its children to be created, put it back in the incomplete nodes list
        if len(remaining_children_to_complete) > 0:
            incompleteNodes[node_name] = remaining_children_to_complete


def find_root():
    for node_name, current_node in nodes.items():
        if current_node.depth == 0:
            return current_node
    return None


# Building tree
tree_file: TextIO = open("in/simpleTree.txt", "r")
creating_nodes_from_file(tree_file)
update_incomplete_nodes()
tree.root = find_root()

print("_____________________")
print("My nodes :")
for name, node in nodes.items():
    print(node.tostring())

print("_____________________")
print("Root is :", tree.root.name)

print("_____________________")
print("Depth-First Search :")
tree.depth_first_search_from_root(give_your_name)

print("_____________________")
print("Breadth-First Search :")
tree.breadth_first_search_from_root(give_your_name)
