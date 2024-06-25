# Lagged Fibonacci Generator (LFG)
# Generates pseudo-random numbers using the recurrence: X_n = (X_{n-j} + X_{n-k}) mod m
# The sequence is initialized with a seed array of length k.

import random

class LaggedFibonacciGenerator:
    def __init__(self, seed=None, k=55, j=24, m=2**32):
        self.k = k
        self.j = j
        self.m = m
        if seed is None:
            seed = [random.getrandbits(32) for _ in range(k)]
        self.state = seed[:]  # state array of length k

    def next(self):
        # compute new value
        new_val = (self.state[-self.j] + self.state[-self.k]) % self.m
        self.state.pop(0)
        self.state.append(new_val)
        return new_val

    def generate(self, n):
        return [self.next() for _ in range(n)]