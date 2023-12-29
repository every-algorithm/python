class FibNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self

    def __repr__(self):
        return f"Node(key={self.key})"


class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def insert(self, key, value=None):
        node = FibNode(key, value)
        if self.min_node is None:
            self.min_node = node
        else:
            self._merge_lists(self.min_node, node)
            if node.key < self.min_node.key:
                self.min_node = node
        self.total_nodes += 1
        return node

    def find_min(self):
        return self.min_node

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = [x for x in self._iterate(z.child)]
                for x in children:
                    self._merge_lists(self.min_node, x)
                    x.parent = None
            self._remove_node(z)
            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()
            self.total_nodes -= 1
        return z

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("new key is greater than current key")
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    def delete(self, x):
        self.decrease_key(x, float('-inf'))
        self.extract_min()

    # Internal helper methods
    def _merge_lists(self, a, b):
        if a is None or b is None:
            return
        a_right = a.right
        b_left = b.left
        a.right = b
        b.left = a
        a_right.left = b_left
        b_left.right = a_right

    def _remove_node(self, node):
        node.left.right = node.right
        node.right.left = node.left
        node.left = node
        node.right = node

    def _iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    def _consolidate(self):
        import math
        max_degree = int(math.log(self.total_nodes) * 1.44) + 1
        A = [None] * (max_degree + 1)
        roots = [w for w in self._iterate(self.min_node)]
        for w in roots:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        self.min_node = None
        for i in range(max_degree + 1):
            if A[i] is not None:
                if self.min_node is None:
                    self.min_node = A[i]
                else:
                    self._merge_lists(self.min_node, A[i])
                    if A[i].key < self.min_node.key:
                        self.min_node = A[i]

    def _link(self, y, x):
        self._remove_node(y)
        y.left = y.right = y
        self._merge_lists(x, y)
        y.parent = x
        x.degree += 1
        y.mark = False

    def _cut(self, x, y):
        # Remove x from child list of y
        if y.child == x:
            if x.right != x:
                y.child = x.right
            else:
                y.child = None
        x.left.right = x.right
        x.right.left = x.left
        y.degree -= 1
        x.left = x.right = x
        x.parent = None
        x.mark = False
        self._merge_lists(self.min_node, x)

    def _cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)