class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children

    def tostring(self):
        res = "Node " + self.name
        if self.children and len(self.children) > 0:
            res += "\n\t" + "Children : "

            for child in self.children:
                res += child.name
                res += ", "

            return res[:-2]
        return res
