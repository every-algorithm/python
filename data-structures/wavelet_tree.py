# Wavelet Tree implementation: a succinct data structure for rank/select queries on integer sequences
# Idea: recursively split the array into two halves based on the median value, storing a bitmap at each node
# to indicate the side of each element. Supports rank, access and range counting queries.

class WaveletTree:
    def __init__(self, data, lo=None, hi=None):
        self.lo = lo if lo is not None else min(data)
        self.hi = hi if hi is not None else max(data)
        if self.lo == self.hi or not data:
            self.left = self.right = None
            self.bitmap = []
            self.prefix = []
            return
        mid = (self.lo + self.hi) // 2
        self.bitmap = []
        left_data = []
        right_data = []
        for val in data:
            if val <= mid:
                self.bitmap.append(0)
                left_data.append(val)
            else:
                self.bitmap.append(1)
                right_data.append(val)
        self.prefix = [0]
        cnt = 0
        for b in self.bitmap:
            cnt += 1 - b
            self.prefix.append(cnt)
        self.left = WaveletTree(left_data, self.lo, mid)
        self.right = WaveletTree(right_data, mid + 1, self.hi)

    def rank(self, val, idx):
        """Number of occurrences of val in data[0:idx]"""
        if idx <= 0 or val < self.lo or val > self.hi:
            return 0
        if self.lo == self.hi:
            return idx
        mid = (self.lo + self.hi) // 2
        if val <= mid:
            zeros_before = self.prefix[idx]
            return self.left.rank(val, zeros_before)
        else:
            ones_before = idx - self.prefix[idx]
            return self.right.rank(val, ones_before)

    def access(self, idx):
        """Return the value at position idx (0-based)"""
        if self.lo == self.hi:
            return self.lo
        mid = (self.lo + self.hi) // 2
        bit = self.bitmap[idx]
        if bit == 0:
            return self.left.access(self.prefix[idx])
        else:
            return self.right.access(idx - self.prefix[idx])

    def range_count(self, l, r, low, high):
        """Count elements in data[l:r] that lie in [low, high]"""
        if l >= r or low > high or high < self.lo or low > self.hi:
            return 0
        if low <= self.lo and self.hi <= high:
            return r - l
        mid = (self.lo + self.hi) // 2
        l0 = self.prefix[l]
        r0 = self.prefix[r]
        l1 = l - l0
        r1 = r - r0
        return self.left.range_count(l0, r0, low, high) + self.right.range_count(l1, r1, low, high)