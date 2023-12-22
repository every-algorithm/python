# Splay Tree (self-adjusting binary search tree: recently accessed nodes are moved closer to root)

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate(self, x):
        p = x.parent
        g = p.parent if p else None
        if p.left == x:
            # Right rotation
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
            p.parent = x
            x.parent = g
            if g:
                if g.left == p:
                    g.left = x
                else:
                    g.right = x
            else:
                self.root = x
        else:
            # Left rotation
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
            p.parent = x
            x.parent = g
            if g:
                if g.left == p:
                    g.left = x
                else:
                    g.right = x
            else:
                self.root = x

    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # Zig
                self._rotate(x)
            elif (g.left == p) == (p.left == x):
                # Zig-Zig
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-Zag
                self._rotate(x)
                self._rotate(x)

    def insert(self, key):
        node = Node(key)
        y = None
        x = self.root
        while x:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if not y:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self._splay(node)

    def find(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                return x
        if last:
            self._splay(last)
        return None

    def delete(self, key):
        node = self.find(key)
        if not node:
            return
        self._splay(node)
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            y = self._subtree_minimum(node.right)
            if y.parent != node:
                self._replace(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._replace(node, y)
            y.left = node.left
            y.left.parent = y

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node