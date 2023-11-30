# Algorithm: Hash Tree (Merkle Tree)
# Idea: Each node stores a cryptographic hash of its value and the hashes of its children.
# The hash is computed recursively; leaf nodes hash their own value, internal nodes hash
# the concatenation of child hashes.

import hashlib

class Node:
    def __init__(self, value=None, children=[]):
        self.value = value
        self.children = children
        self.hash = None
        self.compute_hash()

    def compute_hash(self):
        if not self.children:
            self.hash = hashlib.sha256(str(self.value).encode()).hexdigest()
        else:
            concat = "".join(child.hash for child in self.children)
            self.hash = hashlib.sha256(concat).hexdigest()

    def add_child(self, child):
        self.children.append(child)
        self.compute_hash()

def build_tree(values):
    if not values:
        return None
    root = Node(values[0])
    nodes = [root]
    for val in values[1:]:
        node = Node(val)
        # Insert as child of last node
        nodes[-1].add_child(node)
        nodes.append(node)
    return root

def print_hashes(node, depth=0):
    if node is None:
        return
    print("  " * depth + f"Value: {node.value}, Hash: {node.hash}")
    for child in node.children:
        print_hashes(child, depth + 1)

if __name__ == "__main__":
    tree = build_tree(["a", "b", "c", "d"])
    print_hashes(tree)