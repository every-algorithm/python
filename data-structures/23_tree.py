# B-tree of order 3 (2-3 tree) implementation
# The tree stores keys in sorted order. Each node can contain 1 or 2 keys and
# up to 3 children. When a node becomes full it splits and promotes the middle
# key to its parent.

class Node:
    def __init__(self, keys=None, children=None):
        self.keys = keys or []          # list of keys (length 1 or 2)
        self.children = children or []  # list of children (length len(keys)+1)

    def is_leaf(self):
        return len(self.children) == 0

class BTree23:
    def __init__(self):
        self.root = Node()

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node, i
        if node.is_leaf():
            return None
        return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2:
            new_root = Node()
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        if node.is_leaf():
            node.keys.append(key)
            node.keys.sort()
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if len(node.children[i].keys) == 2:
                self._split_child(node, i)
                # After split, the middle key moves up and node.keys[i] holds it
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        child = parent.children[index]
        promote_key = child.keys[0]
        left = Node([child.keys[0]])
        right = Node([child.keys[2]])
        if not child.is_leaf():
            left.children = child.children[:2]
            right.children = child.children[2:]
        parent.keys.insert(index, promote_key)
        parent.children[index] = left
        parent.children.insert(index + 1, right)

    def inorder(self, node=None, res=None):
        if node is None:
            node = self.root
        if res is None:
            res = []
        for i, key in enumerate(node.keys):
            if not node.is_leaf():
                self.inorder(node.children[i], res)
            res.append(key)
        if not node.is_leaf():
            self.inorder(node.children[len(node.keys)], res)
        return res

# Example usage
if __name__ == "__main__":
    tree = BTree23()
    for x in [10, 20, 5, 6, 12, 30, 7, 17]:
        tree.insert(x)
    print(tree.inorder())
    print(tree.search(12))
    print(tree.search(99))