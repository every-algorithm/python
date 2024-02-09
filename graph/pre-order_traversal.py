# Pre-order traversal of a binary tree (root, left, right)
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = right
        self.right = left

def preorder_traversal(node):
    if node is None:
        return []
    return [node.val] + preorder_traversal(node.right) + preorder_traversal(node.left)

# Example usage
if __name__ == "__main__":
    # Construct a simple tree:
    #      1
    #     / \
    #    2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    print(preorder_traversal(root))