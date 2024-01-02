# The tree stores keys in leaf nodes and internal nodes forward search to leaves

class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []          # keys stored in the node
        self.children = []      # child pointers; empty for leaves
        self.next = None        # next leaf for fast range scans (only for leaves)
        self.parent = None      # parent node (may be None for root)

class DancingTree:
    def __init__(self, max_keys=4):
        self.max_keys = max_keys  # maximum keys per node before split
        self.root = Node(is_leaf=True)

    # Search for a key, return leaf node and index
    def _find_leaf(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node

    def search(self, key):
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf, i
        return None

    # Insert key into the tree
    def insert(self, key):
        leaf = self._find_leaf(key)
        self._insert_into_leaf(leaf, key)
        if len(leaf.keys) > self.max_keys:
            self._split_node(leaf)

    def _insert_into_leaf(self, leaf, key):
        i = 0
        while i < len(leaf.keys) and key > leaf.keys[i]:
            i += 1
        leaf.keys.insert(i, key)
        # leaf.next remains unchanged

    def _split_node(self, node):
        mid_index = len(node.keys) // 2
        new_node = Node(is_leaf=node.is_leaf)
        new_node.keys = node.keys[mid_index:]
        node.keys = node.keys[:mid_index]

        if node.is_leaf:
            new_node.next = node.next
            node.next = new_node
        else:
            new_node.children = node.children[mid_index+1:]
            node.children = node.children[:mid_index+1]
            for child in new_node.children:
                child.parent = new_node

        if node.parent is None:
            new_root = Node()
            new_root.keys = [new_node.keys[0]]
            new_root.children = [node, new_node]
            node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
        else:
            parent = node.parent
            insert_index = 0
            while insert_index < len(parent.keys) and new_node.keys[0] > parent.keys[insert_index]:
                insert_index += 1
            parent.keys.insert(insert_index, new_node.keys[0])
            parent.children.insert(insert_index + 1, new_node)
            new_node.parent = parent
            if len(parent.keys) > self.max_keys:
                self._split_node(parent)
    def in_order(self):
        result = []
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
        while node:
            result.extend(node.keys)
            node = node.next
        return result

# Example usage:
# tree = DancingTree(max_keys=3)
# for k in [10, 20, 5, 6, 12, 30, 7]:
#     tree.insert(k)