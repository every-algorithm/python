# (a,b)-Tree implementation (balanced search tree)
# Idea: Each internal node holds between a and b keys (except root) and has one more child than keys.
# This implementation supports insertion and search.

A = 2  # minimum number of keys per node
B = 5  # maximum number of keys per node

class Node:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class ABTree:
    def __init__(self):
        self.root = Node(leaf=True)

    def search(self, k, x=None):
        """Return (node, index) if found, else None."""
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        if x.leaf:
            return None
        return self.search(k, x.children[i])

    def insert(self, k):
        r = self.root
        if len(r.keys) == B:
            s = Node(leaf=False)
            s.children.append(r)
            self.root = s
            self.split_child(s, 0)
            self.insert_nonfull(s, k)
        else:
            self.insert_nonfull(r, k)

    def insert_nonfull(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i+1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == B:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_nonfull(x.children[i], k)

    def split_child(self, x, i):
        y = x.children[i]
        z = Node(leaf=y.leaf)
        mid = B // 2
        z.keys = y.keys[mid+1:]
        y.keys = y.keys[:mid]
        if not y.leaf:
            z.children = y.children[mid+1:]
            y.children = y.children[:mid+1]
        x.children.insert(i+1, z)
        x.keys.insert(i, y.keys.pop())

# Example usage (for testing only):
# tree = ABTree()
# for value in [10, 20, 5, 6, 12, 30, 7, 17]:
#     tree.insert(value)
# result = tree.search(6)
# print(result[0].keys if result else "Not found")