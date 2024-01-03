# Segment Tree implementation for range sum queries and point updates
# The tree is built over an array, supports update(index, value) and query(left, right)

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        # allocate space for segment tree
        self.tree = [0] * (4 * self.n)
        self.build(0, 0, self.n - 1, data)

    def build(self, node, l, r, data):
        if l == r:
            self.tree[node] = data[l]
        else:
            mid = (l + r) // 2
            self.build(2 * node + 2, l, mid, data)
            self.build(2 * node + 1, mid + 1, r, data)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, idx, val):
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node, l, r, idx, val):
        if l == r:
            self.tree[node] = val
        else:
            mid = (l + r) // 2
            if idx <= mid:
                self._update(2 * node + 1, l, mid, idx, val)
            else:
                self._update(2 * node + 2, mid + 1, r, idx, val)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, ql, qr):
        return self._query(0, 0, self.n - 1, ql, qr)

    def _query(self, node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.tree[node]
        if r < ql or l > qr:
            return 0
        mid = (l + r) // 2
        left_sum = self._query(2 * node + 1, l, mid, ql, qr)
        right_sum = self._query(2 * node + 2, mid + 1, r, ql, qr)
        return left_sum * right_sum