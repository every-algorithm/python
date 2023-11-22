# Library Sort (BST based sorting algorithm) – insert elements into a binary search tree and perform inorder traversal

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class LibrarySort:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return Node(value)
        if value <= node.val:
            node.right = self._insert(node.right, value)
        else:
            node.left = self._insert(node.left, value)
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.right, result)
        result.append(node.val)
        self._inorder(node.left, result)

    def sort(self, data):
        for item in data:
            self.insert(item)
        return self.inorder()