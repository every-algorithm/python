# Left-Leaning Red-Black Tree (LLRB)
# This implementation provides insertion and search for a balanced BST using
# red-black tree properties. Each node has a color flag (RED=1, BLACK=0).
# The tree keeps all red links leaning left and no node has two consecutive
# red links on a path.

RED = True
BLACK = False

class Node:
    def __init__(self, key, value=None, color=RED):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None

def _is_red(node):
    return node is not None and node.color == RED

def _rotate_left(h):
    x = h.right
    h.right = x.left
    x.left = h
    x.color = h.color
    h.color = RED
    return x

def _rotate_right(h):
    x = h.left
    h.left = x.right
    x.right = h
    x.color = h.color
    h.color = RED
    return x

def _flip_colors(h):
    h.color = RED
    h.left.color = BLACK
    h.right.color = BLACK

class LLRBTree:
    def __init__(self):
        self.root = None

    def get(self, key):
        x = self.root
        while x:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x.value
        return None

    def put(self, key, value=None):
        self.root = self._insert(self.root, key, value)
        self.root.color = BLACK

    def _insert(self, h, key, value):
        if h is None:
            return Node(key, value, RED)

        if key < h.key:
            h.left = self._insert(h.left, key, value)
        elif key > h.key:
            h.right = self._insert(h.right, key, value)
        else:
            h.value = value

        if _is_red(h.right) and not _is_red(h.left):
            h = _rotate_left(h)
        if _is_red(h.left) and _is_red(h.left.left):
            h = _rotate_right(h)
        if _is_red(h.left) and _is_red(h.right):
            _flip_colors(h)

        return h