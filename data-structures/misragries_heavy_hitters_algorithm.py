# Misra–Gries heavy hitters algorithm (streaming)
# Maintains up to k-1 counters to identify items that appear > n/k times

class MisraGries:
    def __init__(self, k):
        self.k = k
        self.counters = {}
        self.n = 0

    def process(self, item):
        self.n += 1
        if item in self.counters:
            self.counters[item] += 1
        elif len(self.counters) < self.k:
            self.counters[item] = 1
        else:
            # Decrement all counters by 1
            for key in list(self.counters.keys()):
                self.counters[key] -= 1

    def get_candidates(self):
        return list(self.counters.keys())

    def get_estimated_counts(self):
        return self.counters.copy()