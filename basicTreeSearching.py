from node import Node
from tree import Tree
import json


# Declaring my nodes dictionaries
nodes = {}
incompleteNodes = {}

# Declaring my tree
tree = Tree()


def leaves_first(value):
    return len(value.split(" "))


def creating_nodes_from_file(file):

    lines = file.readlines()

    lines.sort(key=leaves_first)

    for line in lines:

        # removing \n at the end of the line
        line = line[:-1]
        args = line.split(" ")

        node_name = args[0]

        nodes[node_name] = Node(node_name, 0, [None] * len(args[1:]) if len(args) > 1 else None)

        if len(args) > 1:
            node_children_name = args[1:]

            for idx, child in enumerate(node_children_name):

                # If the child have already been created
                if nodes.get(child):
                    nodes[child].increase_depth(nodes[node_name].depth)
                    nodes[node_name].children[idx] = nodes[child]

                # Else, we wait the end to complete the node
                else:

                    if incompleteNodes.get(node_name):
                        children = incompleteNodes[node_name]
                        children.append([child, idx])
                    else:
                        incompleteNodes[node_name] = [[child, idx]]


def update_incomplete_nodes():
    while len(incompleteNodes) > 0:

        node_name, children = incompleteNodes.popitem()

        # Check if all children have been created
        remaining_children_to_complete = []
        for couple in children:
            # A couple is the child name and its position in dad's children list
            child_name = couple[0]
            idx_child = couple[1]

            # If the child exists, just add it to the node children list
            if nodes.get(child_name):
                node = nodes.get(node_name)
                children = nodes[node_name].children
                nodes.get(child_name).increase_depth(node.depth)
                children[idx_child] = nodes.get(child_name)

            # Else, update the list of missing nodes
            else:
                remaining_children_to_complete.append([child_name, idx_child])

        # If my node still needs to wait for its children to be created, put it back in the incomplete nodes list
        if len(remaining_children_to_complete) > 0:
            incompleteNodes[node_name] = remaining_children_to_complete


def find_root():
    for name, node in nodes.items():
        if node.depth == 0:
            return node
    return None


# Building tree
tree_file = open("in/simpleTree.txt", "r")
creating_nodes_from_file(tree_file)
update_incomplete_nodes()
tree.root = find_root()

for name, node in nodes.items():
    print(node.tostring())

print("Root is :", tree.root.name)
