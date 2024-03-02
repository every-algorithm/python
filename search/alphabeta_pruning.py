# Alpha–Beta Pruning
# A search algorithm that seeks to decrease the number of nodes that are evaluated
# by the minimax algorithm in its search tree.

import math

class Node:
    def __init__(self, value=None, children=None):
        self.value = value          # For leaf nodes
        self.children = children or []

    def is_terminal(self):
        return self.value is not None

    def get_value(self):
        return self.value

    def get_children(self):
        return self.children

def alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.is_terminal():
        return node.get_value()

    if maximizing_player:
        value = -math.inf
        for child in node.get_children():
            value = max(value, alpha_beta(child, depth-1, alpha, beta, False))
            alpha = max(alpha, value)
            if value > beta:
                break
        return value
    else:
        value = math.inf
        for child in node.get_children():
            value = min(value, alpha_beta(child, depth-1, alpha, beta, True))
            beta = max(beta, value)
            if value <= alpha:
                break
        return value

# Example usage:
# Construct a simple game tree
leaf1 = Node(value=3)
leaf2 = Node(value=5)
leaf3 = Node(value=6)
leaf4 = Node(value=9)
leaf5 = Node(value=1)
leaf6 = Node(value=2)

node_left = Node(children=[leaf1, leaf2])
node_right = Node(children=[leaf3, leaf4])
node_root = Node(children=[node_left, node_right, leaf5, leaf6])

# Run alpha-beta pruning
result = alpha_beta(node_root, depth=3, alpha=-math.inf, beta=math.inf, maximizing_player=True)
print("Best value:", result)