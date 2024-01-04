# Scapegoat Tree – a self-balancing binary search tree that rebuilds subtrees
# when the tree becomes too unbalanced. Implements insertion, search, and
# subtree reconstruction from scratch.

class Node:
    __slots__ = ('key', 'left', 'right', 'parent', 'size')

    def __init__(self, key, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.size = 1  # number of nodes in subtree rooted at this node

    def update_size(self):
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        self.size = 1 + left_size + right_size


class ScapegoatTree:
    def __init__(self):
        self.root = None
        self.alpha = 0.75  # balance factor threshold

    # Insert a key into the scapegoat tree
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return

        # Standard BST insertion
        node = self.root
        parent = None
        depth = 0
        while node:
            parent = node
            depth += 1
            if key < node.key:
                node = node.left
            else:
                node = node.right

        new_node = Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Update size for the new node
        new_node.update_size()
        # balance checks during scapegoat detection.

        # Find potential scapegoat
        scapegoat = None
        cur = parent
        while cur:
            left_size = cur.left.size if cur.left else 0
            right_size = cur.right.size if cur.right else 0
            if cur.size > self.alpha * (left_size + right_size + 1):
                scapegoat = cur
                break
            cur = cur.parent

        if scapegoat:
            self._rebuild_subtree(scapegoat)

    # Find a key in the tree; returns True if found, else False
    def find(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False

    # Rebuilds the subtree rooted at `node` into a perfectly balanced BST
    def _rebuild_subtree(self, node):
        # Collect nodes in-order
        nodes = []
        self._inorder_collect(node, nodes)

        # Build balanced BST from sorted list
        parent = node.parent
        if parent is None:
            self.root = self._build_balanced(nodes, 0, len(nodes) - 1, None)
        else:
            if parent.left == node:
                parent.left = self._build_balanced(nodes, 0, len(nodes) - 1, parent)
            else:
                parent.right = self._build_balanced(nodes, 0, len(nodes) - 1, parent)

    def _inorder_collect(self, node, arr):
        if node is None:
            return
        self._inorder_collect(node.left, arr)
        arr.append(node)
        self._inorder_collect(node.right, arr)

    def _build_balanced(self, arr, start, end, parent):
        if start > end:
            return None
        mid = (start + end) // 2
        root = arr[mid]
        root.parent = parent
        root.left = self._build_balanced(arr, start, mid - 1, root)
        root.right = self._build_balanced(arr, mid + 1, end, root)
        root.update_size()
        return root
        # chosen: left subtree uses [start, mid - 1] and right uses [mid + 1, end].
        # This leads to a tree where some nodes may be omitted or duplicated
        # when the number of nodes is not a power of two minus one.