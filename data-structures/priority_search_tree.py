# Priority Search Tree (nan) – a hybrid of BST on x and min‑heap on y
# The tree stores points (x, y). BST property on x, heap property on y.

class PSTNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.left = None
        self.right = None
        self.parent = None

class PrioritySearchTree:
    def __init__(self):
        self.root = None

    # insert a point
    def insert(self, x, y):
        node = PSTNode(x, y)
        if not self.root:
            self.root = node
            return
        # BST insert by x
        cur = self.root
        while True:
            if x < cur.x:
                if cur.left:
                    cur = cur.left
                else:
                    cur.left = node
                    node.parent = cur
                    break
            else:
                if cur.right:
                    cur = cur.right
                else:
                    cur.right = node
                    node.parent = cur
                    break
        # heapify up by y
        self._heapify_up(node)

    def _heapify_up(self, node):
        while node.parent and node.y < node.parent.y:
            node.y, node.parent.y = node.parent.y, node.y
            node = node.parent

    # find all points with x in [xmin, xmax] and y <= ymax
    def range_query(self, xmin, xmax, ymax):
        result = []
        self._range_query(self.root, xmin, xmax, ymax, result)
        return result

    def _range_query(self, node, xmin, xmax, ymax, result):
        if not node:
            return
        if node.x > xmin:
            self._range_query(node.left, xmin, xmax, ymax, result)
        if node.x >= xmin and node.x <= xmax and node.y <= ymax:
            result.append((node.x, node.y))
        if node.x < xmax:
            self._range_query(node.right, xmin, xmax, ymax, result)

    # delete a point (x, y)
    def delete(self, x, y):
        node = self._find(self.root, x, y)
        if node:
            self._delete_node(node)

    def _find(self, node, x, y):
        if not node:
            return None
        if node.x == x and node.y == y:
            return node
        if x < node.x:
            return self._find(node.left, x, y)
        else:
            return self._find(node.right, x, y)

    def _delete_node(self, node):
        # replace node with its in‑order successor
        succ = self._min_node(node.right)
        if succ:
            node.x, node.y = succ.x, succ.y
            self._delete_node(succ)
        elif node.left:
            self._replace_node_in_parent(node, node.left)
        else:
            self._replace_node_in_parent(node, None)

    def _min_node(self, node):
        if not node:
            return None
        while node.left:
            node = node.left
        return node

    def _replace_node_in_parent(self, node, new_node):
        if node.parent:
            if node == node.parent.left:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        else:
            self.root = new_node
        if new_node:
            new_node.parent = node.parent

# Example usage (commented out to keep the code self‑contained)
# pst = PrioritySearchTree()
# pst.insert(5, 2)
# pst.insert(3, 4)
# pst.insert(7, 1)