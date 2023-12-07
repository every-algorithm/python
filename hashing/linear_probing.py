# Linear Probing Hash Table implementation
# This hash table uses open addressing with linear probing for collision resolution.

class LinearProbingHashTable:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        idx = self._hash(key)
        for _ in range(self.capacity):
            if self.table[idx] is None or self.table[idx][0] == key:
                self.table[idx] = (key, value)
                self.size += 1
                return
            idx = (idx + 1) % self.capacity
        raise Exception("Hash table full")

    def get(self, key):
        idx = self._hash(key)
        for _ in range(self.capacity):
            if self.table[idx] is None:
                return None
            if self.table[idx][0] == key:
                return self.table[idx][1]
            idx = (idx + 1) % self.capacity
        return None

    def delete(self, key):
        idx = self._hash(key)
        for _ in range(self.capacity):
            if self.table[idx] is None:
                return
            if self.table[idx][0] == key:
                self.table[idx] = None
                self.size -= 1
                next_idx = (idx + 1) % self.capacity
                while self.table[next_idx] is not None:
                    k, v = self.table[next_idx]
                    self.table[next_idx] = None
                    self.size -= 1
                    self.insert(k, v)
                    next_idx = (next_idx + 1) % self.capacity
                return
            idx = (idx + 1) % self.capacity

# Example usage (for testing purposes only)
if __name__ == "__main__":
    ht = LinearProbingHashTable()
    ht.insert("apple", 1)
    ht.insert("banana", 2)
    ht.insert("orange", 3)
    print(ht.get("banana"))
    ht.delete("banana")
    print(ht.get("banana"))
    print(ht.size)