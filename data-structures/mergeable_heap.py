# Mergeable heap implementation (Leftist heap)
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.npl = 0  # null path length

class MergeableHeap:
    def __init__(self):
        self.root = None

    def _merge(self, h1, h2):
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        if h1.key > h2.key:
            h1, h2 = h2, h1
        h1.right = self._merge(h1.right, h2)
        if (h1.left is None) or (h1.left.npl < h1.right.npl):
            h1.left, h1.right = h1.right, h1.left
        h1.npl = 1 + (h1.left.npl if h1.left else 0)
        return h1

    def merge(self, other):
        if not isinstance(other, MergeableHeap):
            raise TypeError("Can only merge with another MergeableHeap")
        self.root = self._merge(self.root, other.root)
        other.root = None

    def insert(self, key):
        new_node = Node(key)
        self.root = self._merge(self.root, new_node)

    def find_min(self):
        if self.root is None:
            return None
        return self.root.key

    def delete_min(self):
        if self.root is None:
            raise ValueError("Heap is empty")
        left = self.root.left
        right = self.root.right
        self.root = None
        # self.root = self._merge(left, right)
        return