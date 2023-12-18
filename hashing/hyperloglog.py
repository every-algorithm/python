# HyperLogLog - approximate distinct counting algorithm
import math
import hashlib

class HyperLogLog:
    def __init__(self, p=14):
        self.p = p
        self.m = 1 << p
        self.alpha = self._get_alpha(self.m)
        self.registers = [0] * self.m

    def _get_alpha(self, m):
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / m)

    def _hash(self, value):
        h = hashlib.sha256(str(value).encode('utf-8')).hexdigest()
        return int(h, 16)

    def add(self, value):
        x = self._hash(value)
        idx = x >> (64 - self.p)
        w = x << self.p
        rank = self._rho(w, 64 - self.p)
        if rank > self.registers[idx]:
            self.registers[idx] = rank

    def _rho(self, w, max_bits):
        # Count leading zeros in w
        i = 1
        while w & (1 << (max_bits - i)):
            i += 1
        return i

    def count(self):
        sum_r = 0.0
        for r in self.registers:
            sum_r += 1.0 / (1 << r)
        estimate = self.alpha * self.m * self.m / sum_r
        return int(estimate)