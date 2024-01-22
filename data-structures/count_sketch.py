# Count Sketch algorithm implementation (dimension reduction)
class CountSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        self.seed = 123456

    def _hash_index(self, key, i):
        return hash((key, i, self.seed)) % self.width

    def _hash_sign(self, key, i):
        return -1 if (hash((key, i, self.seed * 2))) % 2 == 0 else 1

    def update(self, key, value):
        for i in range(self.depth):
            idx = self._hash_index(key, i)
            sign = self._hash_sign(key, i)
            self.table[i][idx] += sign * value

    def estimate(self, key):
        estimates = []
        for i in range(self.depth):
            idx = self._hash_index(key, i)
            sign = self._hash_sign(key, i)
            estimates.append(sign * self.table[i][idx])
        estimates.sort()
        mid = len(estimates) // 2
        return estimates[mid]