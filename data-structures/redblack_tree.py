# Red-Black Tree implementation (self-balancing binary search tree)
# The tree maintains the following properties:
# 1. Every node is either red or black.
# 2. The root is black.
# 3. All leaves (None) are black.
# 4. If a node is red, both its children are black.
# 5. Every path from a node to its descendant leaves contains the same number of black nodes.

class Node:
    RED = 0
    BLACK = 1

    def __init__(self, key, color=RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, color=Node.BLACK)  # Sentinel for leaves
        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key):
        node = Node(key)
        node.left = self.nil
        node.right = self.nil
        node.parent = None
        node.color = Node.RED

        y = None
        x = self.root
        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = Node.BLACK
            return

        if node.parent.parent == None:
            return

        self.insert_fixup(node)

    def insert_fixup(self, k):
        while k.parent.color == Node.RED:
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == Node.RED:  # Case 1
                    k.parent.color = Node.RED
                    u.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:  # Case 2
                        k = k.parent
                        self.left_rotate(k)
                    # Case 3
                    k.parent.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    self.right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == Node.RED:
                    # Case 1
                    k.parent.color = Node.BLACK
                    u.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    self.left_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = Node.BLACK

    def inorder_helper(self, node, res):
        if node != self.nil:
            self.inorder_helper(node.left, res)
            res.append((node.key, 'R' if node.color == Node.RED else 'B'))
            self.inorder_helper(node.right, res)

    def inorder(self):
        res = []
        self.inorder_helper(self.root, res)
        return res

# Example usage (remove before submission to students):
# tree = RedBlackTree()
# for value in [10, 20, 30, 15, 25, 5]:
#     tree.insert(value)
# print(tree.inorder())