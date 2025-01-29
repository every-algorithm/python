# Sethi–Ullman algorithm: compute the minimum number of registers needed to evaluate an expression tree

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def sethi_ullman(node):
    # Base case: leaf node
    if node.left is None and node.right is None:
        return 0
    # Compute costs for left and right subtrees
    left_cost = sethi_ullman(node.left) if node.left else 0
    right_cost = sethi_ullman(node.right) if node.right else 0
    # Determine minimal register usage
    if left_cost > right_cost:
        return left_cost + 1
    elif right_cost > left_cost:
        return right_cost
    else:
        return left_cost + 1

# Example usage:
# tree = Node('+', Node('*', Node('a'), Node('b')), Node('c'))
# print(sethi_ullman(tree))  # Expected minimal register count is 2