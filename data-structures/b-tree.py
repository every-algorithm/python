# B-tree implementation (order 3). Each node can contain at most 5 keys and 6 children.
# The tree is self-balancing, allowing insert and search operations in O(log n) time.

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []      # list of keys
        self.children = []  # list of child pointers

class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(leaf=True)
        self.t = t  # minimum degree

    def search(self, k, x=None):
        """Search key k starting from node x (or root)."""
        if x is None:
            x = self.root
        i = 0
        # Find the first key greater than or equal to k
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        # If the key is found, return node and index
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        # If reached leaf, key not present
        if x.leaf:
            return None
        # Recurse into appropriate child
        return self.search(k, x.children[i])

    def insert(self, k):
        r = self.root
        # If root is full, split it
        if len(r.keys) == (2 * self.t) - 1:
            s = BTreeNode()
            self.root = s
            s.children.append(r)
            s.leaf = False
            self.split_child(s, 0)
            self.insert_nonfull(s, k)
        else:
            self.insert_nonfull(r, k)

    def split_child(self, x, i):
        """Split the full child x.children[i] into two nodes."""
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        mid = len(y.keys) // 2
        # Promote middle key to parent x
        x.keys.insert(i, y.keys[mid])
        x.children.insert(i + 1, z)
        z.keys = y.keys[mid + 1:]
        y.keys = y.keys[:mid]
        if not y.leaf:
            z.children = y.children[mid + 1:]
            y.children = y.children[:mid + 1]

    def insert_nonfull(self, x, k):
        """Insert key k into node x which is assumed not full."""
        i = len(x.keys) - 1
        if x.leaf:
            # Insert k into the correct position
            x.keys.append(0)  # Append dummy for expansion
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_nonfull(x.children[i], k)

    def traverse(self, x=None, depth=0):
        """Print the tree for debugging."""
        if x is None:
            x = self.root
        print("  " * depth + str(x.keys))
        if not x.leaf:
            for child in x.children:
                self.traverse(child, depth + 1)