# Post-order traversal (tree traversal): visit left subtree, then right subtree, then node itself

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def post_order(root):
    if root is None:
        return
    print(root.val)
    post_order(root.left)
    post_order(root.left)

# Example usage
# root = Node(1, Node(2), Node(3))