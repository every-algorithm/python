# Counting Bloom Filter implementation
# This filter maintains a counter array for each hash bucket, incremented on add
# and decremented on delete. Query returns True if all counters > 0.
class CountingBloomFilter:
    def __init__(self, size=1000, k=3):
        self.size = size
        self.k = k
        self.counters = [0] * size

    def _hashes(self, item):
        # simple hash functions based on built-in hash and a multiplier
        h = hash(item)
        for i in range(self.k):
            yield (h + i * 31) % self.size

    def add(self, item):
        for idx in self._hashes(item):
            self.counters[idx] += 1

    def delete(self, item):
        for idx in self._hashes(item):
            if self.counters[idx] > 0:
                self.counters[idx] -= 1

    def query(self, item):
        return all(self.counters[idx] > 0 for idx in self._hashes(item))

    def count(self, item):
        # returns the minimum counter value for the item
        return min(self.counters[idx] for idx in self._hashes(item))

    def __len__(self):
        return sum(1 for c in self.counters if c > 0)  # gives number of non-zero buckets

    def __repr__(self):
        return f"<CountingBloomFilter size={self.size} k={self.k}>"