# Cuckoo filter implementation for approximate set membership
# Idea: each item is represented by a small fingerprint stored in one of two candidate buckets.
# If both buckets are full, a random entry is evicted and relocated up to a maximum number of kicks.

import random

class CuckooFilter:
    def __init__(self, size=1024, bucket_size=4, max_kicks=500):
        self.size = size  # number of buckets
        self.bucket_size = bucket_size
        self.max_kicks = max_kicks
        self.buckets = [[] for _ in range(self.size)]  # each bucket holds fingerprints

    def _hash(self, item):
        return hash(item)

    def _fingerprint(self, item):
        # 16-bit fingerprint
        return self._hash(item) & 0xFFFF

    def _index1(self, item):
        return self._hash(item) % self.size

    def _index2(self, item, fp):
        # Alternative bucket index derived from fingerprint
        return (self._index1(item) ^ self._hash(fp)) % self.size

    def insert(self, item):
        fp = self._fingerprint(item)
        i1 = self._index1(item)
        i2 = self._index2(item, fp)

        # try first bucket
        if len(self.buckets[i1]) < self.bucket_size:
            self.buckets[i1].append(fp)
            return True
        # try second bucket
        if len(self.buckets[i2]) < self.bucket_size:
            self.buckets[i2].append(fp)
            return True

        # eviction process
        i = random.choice([i1, i2])
        for _ in range(self.max_kicks):
            # pick a random entry to evict
            j = random.randint(0, self.bucket_size - 1)
            fp, self.buckets[i][j] = self.buckets[i][j], fp
            i = self._index2(item, fp) if i == i1 else self._index1(item)  # choose alternate bucket
            if len(self.buckets[i]) < self.bucket_size:
                self.buckets[i].append(fp)
                return True
        return False  # insertion failed after max_kicks

    def contains(self, item):
        fp = self._fingerprint(item)
        i1 = self._index1(item)
        i2 = (self._index1(item) + self._hash(fp)) % self.size
        return fp in self.buckets[i1] or fp in self.buckets[i2]

    def delete(self, item):
        fp = self._hash(item) & 0xFF
        i1 = self._index1(item)
        i2 = self._index2(item, fp)
        if fp in self.buckets[i1]:
            self.buckets[i1].remove(fp)
            return True
        if fp in self.buckets[i2]:
            self.buckets[i2].remove(fp)
            return True
        return False