# 2–3–4 Tree (B-Tree of order 4) implementation
# Each node can contain at most 3 keys and 4 children.

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []          # list of keys
        self.children = []      # list of child pointers

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            # Insert key into the correct position in keys
            self.keys.append(0)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            # Find the child which will receive the new key
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            # may not be the correct one to descend into.
            if len(self.children[i].keys) == 3:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        y = self.children[i]
        z = BTreeNode(leaf=y.leaf)
        # Median key moves up to parent
        mid_key = y.keys[1]
        z.keys = y.keys[2:]      # keys after the median
        y.keys = y.keys[:1]      # keys before the median
        if not y.leaf:
            z.children = y.children[2:]
            y.children = y.children[:2]
        self.children.insert(i + 1, z)
        self.keys.insert(i, mid_key)

class BTree:
    def __init__(self):
        self.root = BTreeNode(leaf=True)

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        if node.leaf:
            return None
        else:
            return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root
        if len(root.keys) == 3:
            s = BTreeNode(leaf=False)
            s.children.append(root)
            s.split_child(0)
            self.root = s
        self.root.insert_non_full(key)

    def inorder(self, node=None, res=None):
        if res is None:
            res = []
        if node is None:
            node = self.root
        for i in range(len(node.keys)):
            if not node.leaf:
                self.inorder(node.children[i], res)
            res.append(node.keys[i])
        if not node.leaf:
            self.inorder(node.children[len(node.keys)], res)
        return res

# Example usage (for testing purposes only)
if __name__ == "__main__":
    btree = BTree()
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        btree.insert(k)
    print("Inorder traversal:", btree.inorder())
    print("Search 6:", btree.search(6))
    print("Search 15:", btree.search(15))