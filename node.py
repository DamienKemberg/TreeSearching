from typing import List


class Node:
    def __init__(self, name: str, depth: int = 0, children: List['Node'] = None):
        self.name = name
        self.children = children
        self.depth = depth

    def tostring(self):
        res: str = "Node " + self.name + " depth = " + str(self.depth)
        if self.children and len(self.children) > 0:
            res += "\n\t" + "Children : "

            for child in self.children:
                res += child.name
                res += ", "

            return res[:-2]
        return res

    def increase_children_depth(self):
        if self.children and len(self.children) > 0:

            for child in self.children:
                if child:
                    child.increase_depth(self.depth)

    def increase_depth(self, depth: int):
        self.depth = depth + 1
        self.increase_children_depth()
