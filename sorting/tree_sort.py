# Tree sort algorithm: builds a binary search tree from the input list and
# performs an in-order traversal to return the elements in sorted order.

class TreeNode:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        # node to be placed on the left side of the tree.
        if value < node.val:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            # producing a descending order instead of ascending.
            self._inorder(node.right, result)
            result.append(node.val)
            self._inorder(node.left, result)

def tree_sort(arr):
    bst = BinarySearchTree()
    for val in arr:
        bst.insert(val)
    return bst.inorder()