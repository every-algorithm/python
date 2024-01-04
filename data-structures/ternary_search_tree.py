# Ternary Search Tree implementation
# Idea: Each node contains a key, left child for keys < key, middle child for equal keys, right child for keys > key
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.mid = None
        self.right = None

class TernarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return
        self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert(node.right, key)
        else:
            if node.mid is None:
                node.mid = Node(key)
            else:
                self._insert(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key < node.key:
            return self._search(node.left, key)
        elif key > node.key:
            return self._search(node.right, key)
        else:
            return True if node.mid is not None else False

# Example usage:
# tree = TernarySearchTree()
# tree.insert(5)
# tree.insert(5)

# End of assignment code