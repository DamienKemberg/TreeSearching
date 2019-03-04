from node import Node
from typing import Callable, List
from collections import deque

class Tree:

    def __init__(self, root: Node=None):
        self.root = root

    def breadth_first_search_from_root(self, treatment: Callable[[Node], None]):
        pile: deque[Node] = deque([self.root])

        while len(pile) > 0:
            node = pile.popleft()
            treatment(node)

            if node.children:
                for child in node.children:
                    pile.append(child)

    def depth_first_search(self, node: Node, treatment: Callable[[Node], None]):
        treatment(node)

        if node.children:
            for child in node.children:
                self.depth_first_search(child, treatment)

    def depth_first_search_from_root(self, treatment: Callable[[Node], None]):
        self.depth_first_search(self.root, treatment)
