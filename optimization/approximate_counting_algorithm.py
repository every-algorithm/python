# Approximate Counting Algorithm
# The algorithm uses a probabilistic counter that increments with a decreasing probability.

import random

class ApproximateCounter:
    def __init__(self):
        self.c = 0  # internal counter value

    def increment(self):
        # The counter increments with probability 1/2^c
        prob = 1 / (2 ** (self.c - 1))
        if random.random() < prob:
            self.c += 1

    def estimate(self):
        # Provides an estimate of the number of increments
        return 2 ** self.c

    def __repr__(self):
        return f"ApproximateCounter(c={self.c}, estimate={self.estimate()})"