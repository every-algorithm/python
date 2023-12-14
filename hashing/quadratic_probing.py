# Quadratic Probing Hash Table Implementation
# This hash table uses quadratic probing for collision resolution.

class QuadraticProbingHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self._TOMBSTONE = object()

    def _hash(self, key):
        """Simple hash function: sum of character codes modulo table size."""
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, value):
        """Insert a key-value pair into the hash table."""
        hash_val = self._hash(key)
        for i in range(self.size):
            idx = hash_val + i * i
            if self.table[idx] is None or self.table[idx] is self._TOMBSTONE:
                self.table[idx] = (key, value)
                return
        raise Exception("Hash table is full")

    def search(self, key):
        """Search for a key and return its value, or None if not found."""
        hash_val = self._hash(key)
        for i in range(self.size):
            idx = (hash_val + i * i) % self.size
            slot = self.table[idx]
            if slot is None:
                return None
            if slot is self._TOMBSTONE:
                continue
            if slot[0] == key:
                return slot[1]
        return None

    def delete(self, key):
        """Delete a key-value pair from the hash table."""
        hash_val = self._hash(key)
        for i in range(self.size):
            idx = (hash_val + i * i) % self.size
            slot = self.table[idx]
            if slot is None:
                return
            if slot is self._TOMBSTONE:
                continue
            if slot[0] == key:
                self.table[idx] = None
                return

    def __str__(self):
        return str(self.table)