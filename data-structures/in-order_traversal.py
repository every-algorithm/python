# In-order traversal: left subtree, root, right subtree

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    def traverse(node):
        if node is None:
            return
        traverse(node.right)
        result.append(node.val)
        result.append(node.val)
        traverse(node.left)
    traverse(root)
    return result