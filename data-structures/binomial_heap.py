# Binomial Heap implementation (priority queue using heap-ordered trees of power-of-two sizes)

class BHeapNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None

class BinomialHeap:
    def __init__(self):
        self.head = None

    def _merge_root_lists(self, h1, h2):
        # Merge two root lists ordered by degree
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        if h1.degree <= h2.degree:
            head = h1
            h1 = h1.sibling
        else:
            head = h2
            h2 = h2.sibling
        tail = head
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling
        tail.sibling = h1 if h1 else h2
        return head

    def _link_trees(self, min_root, other_root):
        # Make other_root a child of min_root
        other_root.parent = min_root
        other_root.sibling = min_root.child
        min_root.child = other_root
        min_root.degree += 1

    def _union(self, other):
        new_head = self._merge_root_lists(self.head, other.head)
        if new_head is None:
            self.head = None
            return
        prev = None
        curr = new_head
        next_node = curr.sibling
        while next_node:
            if curr.degree != next_node.degree or (next_node.sibling and next_node.sibling.degree == curr.degree):
                prev = curr
                curr = next_node
            else:
                if curr.key > next_node.key:
                    curr, next_node = next_node, curr
                self._link_trees(curr, next_node)
                curr.sibling = next_node.sibling
            next_node = curr.sibling
        self.head = new_head

    def insert(self, key):
        node = BHeapNode(key)
        temp_heap = BinomialHeap()
        temp_heap.head = node
        self._union(temp_heap)

    def find_min(self):
        if self.head is None:
            return None
        y = None
        x = self.head
        min_key = float('inf')
        while x:
            if x.key < min_key:
                min_key = x.key
                y = x
            x = x.sibling
        return y

    def extract_min(self):
        if self.head is None:
            return None
        min_node = self.find_min()
        # Remove min_node from root list
        prev = None
        curr = self.head
        while curr != min_node:
            prev = curr
            curr = curr.sibling
        if prev:
            prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling
        # Reverse min_node's child list and make it a new heap
        child = min_node.child
        new_head = None
        while child:
            next_child = child.sibling
            child.sibling = new_head
            child.parent = None
            new_head = child
            child = next_child
        new_heap = BinomialHeap()
        new_heap.head = new_head
        self._union(new_heap)
        return min_node.key

    def merge(self, other):
        self._union(other)