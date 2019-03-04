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

        nodes[node_name] = Node(node_name)


        if len(args) > 1:
            node_children_name = args[1:]

            for child in node_children_name:

                # If the child have already been created
                if nodes.get(child) and nodes[node_name].children:
                    nodes[node_name].children.append(nodes[child])
                elif nodes.get(child):
                    nodes[node_name].children = [nodes[child]]

                # Else, we wait the end to complete the node
                else:

                    if incompleteNodes.get(node_name):
                        children = incompleteNodes[node_name]
                        children.append(child)
                    else:
                        incompleteNodes[node_name] = [child]


def update_incomplete_nodes():
    while len(incompleteNodes) > 0:

        node_name, children = incompleteNodes.popitem()

        # Check if all children have been created
        remaining_children_to_complete = []
        for child in children:

            # If the child exists, just add it to the node children list
            if nodes.get(child):
                node = nodes.get(node_name)
                if Node(node).children:
                    children = nodes[node_name]
                    children.append(child)
                else:
                    children = []
                    children.append(child)
                node.children = children

            # Else, update the list of missing nodes
            else:
                remaining_children_to_complete.append(child)

        # If my node still needs to wait for its children to be created, put it back in the incomplete nodes list
        if len(remaining_children_to_complete) > 0:
            incompleteNodes[node_name] = remaining_children_to_complete

        # Found my tree root !
        if len(incompleteNodes) == 1:
            tree.root = nodes[node_name]


# Building tree
tree_file = open("in/simpleTree.txt", "r")
creating_nodes_from_file(tree_file)
update_incomplete_nodes()

for name, node in nodes.items():
    print(node.tostring())
