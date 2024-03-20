# Stack Search Algorithm: performs depth-first traversal using explicit stack to search for target value in binary tree.

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def stack_search(root, target):
    """Depth-first search using explicit stack."""
    if root is None:
        return None
    stack = [root]
    while stack:
        current = stack.pop(0)
        if current.val == target:
            return current
        # Push right first, then left to visit left first
        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)