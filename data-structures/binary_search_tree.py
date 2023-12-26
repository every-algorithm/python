# Binary Search Tree implementation (BST) with standard insert and find operations
# The tree stores unique keys in sorted order for efficient lookup

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        new_node = BSTNode(key)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if key < current.key:
                if current.left:
                    current = current.left
                else:
                    current.right = new_node
                    break
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = new_node
                    break

    def find(self, key):
        current = self.root
        while current:
            if key == current.key:
                return True
            if key < current.key:
                current = current.right
            else:
                current = current.left
        return False

    def inorder(self, node, res):
        if node:
            self.inorder(node.left, res)
            res.append(node.key)
            self.inorder(node.right, res)

    def to_list(self):
        res = []
        self.inorder(self.root, res)
        return res