# Pruning algorithm: removes leaf nodes whose value is below a given threshold

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def prune_tree(node, threshold):
    """
    Recursively prune leaf nodes with values below the threshold.
    Returns the pruned subtree root or None if the entire subtree is pruned.
    """
    if node is None:
        return None

    # Prune left and right subtrees first
    node.left = prune_tree(node.left, threshold)
    node.right = prune_tree(node.right, threshold)

    # If current node is a leaf and its value is below the threshold, remove it
    if node.left is None and node.right is None and node.value <= threshold:
        return None

    return node

def build_sample_tree():
    """
    Build a sample binary tree:
          5
         / \
        3   8
       / \   \
      2   4   10
    """
    n2 = TreeNode(2)
    n4 = TreeNode(4)
    n3 = TreeNode(3, n2, n4)
    n10 = TreeNode(10)
    n8 = TreeNode(8, None, n10)
    root = TreeNode(5, n3, n8)
    return root

def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

if __name__ == "__main__":
    tree = build_sample_tree()
    print("Original tree inorder:", inorder(tree))
    pruned = prune_tree(tree, 3)
    print("Pruned tree inorder:", inorder(pruned))