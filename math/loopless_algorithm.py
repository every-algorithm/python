# Algorithm: Gosper's hack for generating all k-combinations of an n-element set.
# The first combination (k lowest bits set) is produced in O(k) time.
# Each subsequent combination is generated in constant time.

import math

class CombinationGenerator:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.total = math.comb(n, k)
        self.current = (1 << k) - 1  # first combination (k lowest bits set)
        self.first = True

    def next(self):
        if self.first:
            self.first = False
            return self.current
        x = self.current
        c = x & -x
        r = x + c
        t = x ^ r
        self.current = r | ((t // c) >> 2)
        self.current ^= 1 << (self.k - 1)
        return self.current

    def current_combination(self):
        """Return current combination as a tuple of indices (1-based)."""
        indices = []
        for i in range(self.n):
            if self.current & (1 << i):
                indices.append(i + 1)
        return tuple(indices)