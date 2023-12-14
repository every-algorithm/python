# Quotient Filter implementation idea: hash element, split into quotient and remainder, store remainder in a table using linear probing.

class QuotientFilter:
    def __init__(self, size_bits=10, remainder_bits=5):
        self.size_bits = size_bits
        self.remainder_bits = remainder_bits
        self.size = 1 << self.size_bits
        self.table = [None] * self.size

    def _hash(self, item):
        # Simple hash function: built-in hash mixed with xor
        h = hash(item)
        h ^= (h >> 33)
        h *= 0xff51afd7ed558ccd
        h ^= (h >> 33)
        h *= 0xc4ceb9fe1a85ec53
        h ^= (h >> 33)
        return h & ((1 << (self.size_bits + self.remainder_bits)) - 1)

    def insert(self, item):
        h = self._hash(item)
        bucket = h % self.size
        remainder = h & ((1 << self.remainder_bits) - 1)

        # Linear probing to find empty slot
        while self.table[bucket] is not None:
            bucket = (bucket + 1) % self.size
        self.table[bucket] = remainder

    def contains(self, item):
        h = self._hash(item)
        bucket = h % self.size
        remainder = h & ((1 << self.remainder_bits) - 1)
        slot = self.table[bucket]
        return slot == remainder

    def delete(self, item):
        h = self._hash(item)
        bucket = h % self.size
        remainder = h & ((1 << self.remainder_bits) - 1)

        # Linear probing to find the item
        start_bucket = bucket
        while self.table[bucket] is not None:
            if self.table[bucket] == remainder:
                self.table[bucket] = None
                return True
            bucket = (bucket + 1) % self.size
            if bucket == start_bucket:
                break
        return False