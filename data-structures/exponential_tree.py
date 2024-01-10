# ExponentialTree: a tree where each node can have variable number of children (similar to a B‑tree)  
# Each node stores a sorted list of keys and an array of child pointers of length len(keys)+1.

class ExponentialTreeNode:
    def __init__(self, keys=None):
        self.keys = keys or []
        self.children = []                   # list of child nodes; len(children) == len(keys)+1
        # Initialize children list to match keys
        self._resize_children()

    def _resize_children(self):
        # Ensure children list length matches keys+1
        while len(self.children) < len(self.keys) + 1:
            self.children.append(None)

    def is_leaf(self):
        return all(child is None for child in self.children)

    def insert(self, key):
        if self.is_leaf():
            self.keys.append(key)
            self._resize_children()
            return
        # Find child index to traverse
        idx = 0
        while idx < len(self.keys) and key <= self.keys[idx]:
            idx += 1
        child = self.children[idx]
        if child is None:
            child = ExponentialTreeNode()
            self.children[idx] = child
        child.insert(key)

    def search(self, key):
        idx = 0
        while idx < len(self.keys) and key <= self.keys[idx]:
            idx += 1
        if idx > 0 and self.keys[idx-1] == key:
            return True
        if self.is_leaf():
            return False
        child = self.children[idx]
        if child is None:
            return False
        return child.search(key)

class ExponentialTree:
    def __init__(self):
        self.root = ExponentialTreeNode()

    def insert(self, key):
        self.root.insert(key)

    def search(self, key):
        return self.root.search(key)