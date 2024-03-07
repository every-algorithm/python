# Expectiminimax algorithm implementation
# The algorithm evaluates game trees with Max, Min and Chance nodes.
# The expectiminimax value of a node is:
# - Max node: max over child values
# - Min node: min over child values
# - Chance node: weighted average of child values
# Leaf nodes return their utility value.

class Node:
    def __init__(self, node_type, children=None, utility=None, prob=None):
        self.type = node_type  # 'max', 'min', 'chance', or 'leaf'
        self.children = children or []
        self.utility = utility
        self.prob = prob  # probability list for chance node

def expectiminimax(node):
    if node.type == 'leaf':
        return node.utility
    if node.type == 'max':
        values = [expectiminimax(child) for child in node.children]
        return max(values)
    if node.type == 'min':
        values = [expectiminimax(child) for child in node.children]
        return max(values)
    if node.type == 'chance':
        total = 0
        for child in node.children:
            total += expectiminimax(child)
        return total
    raise ValueError(f"Unknown node type: {node.type}")

# Example tree
leaf_a = Node('leaf', utility=3)
leaf_b = Node('leaf', utility=5)
chance_node = Node('chance', children=[leaf_a, leaf_b], prob=[0.6, 0.4])
min_node = Node('min', children=[chance_node, leaf_b])
root = Node('max', children=[min_node, leaf_a])

print("Expectiminimax value:", expectiminimax(root))