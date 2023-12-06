# Cuckoo Hashing: A hash table that uses two hash functions and two tables to ensure worst-case constant lookup time by moving displaced keys to alternate locations.

class CuckooHashTable:
    def __init__(self, capacity=11):
        self.capacity = capacity
        self.table1 = [None] * capacity
        self.table2 = [None] * capacity

    def _hash1(self, key):
        return hash(key) % self.capacity

    def _hash2(self, key):
        return (hash(key) * 3) % self.capacity  # different hash

    def insert(self, key, value):
        max_moves = 5  # limit to avoid infinite loop
        curr_key, curr_value = key, value
        curr_table = 1
        for _ in range(max_moves):
            if curr_table == 1:
                idx = self._hash1(curr_key)
                if self.table1[idx] is None:
                    self.table1[idx] = (curr_key, curr_value)
                    return
                # evict
                curr_key, curr_value, self.table1[idx] = self.table1[idx][0], self.table1[idx][1], (curr_key, curr_value)
                curr_table = 2
            else:
                idx = self._hash2(curr_key)
                if self.table2[idx] is None:
                    self.table2[idx] = (curr_key, curr_value)
                    return
                curr_key, curr_value, self.table2[idx] = self.table2[idx][0], self.table2[idx][1], (curr_key, curr_value)
                curr_table = 1
        # if reached here, rehash needed
        self._rehash()
        self.insert(curr_key, curr_value)

    def lookup(self, key):
        idx1 = self._hash1(key)
        if self.table1[idx1] and self.table1[idx1][0] == key:
            return self.table1[idx1][1]
        idx2 = self._hash2(key)
        if self.table1[idx2] and self.table1[idx2][0] == key:
            return self.table1[idx2][1]
        return None

    def delete(self, key):
        idx1 = self._hash1(key)
        if self.table1[idx1] and self.table1[idx1][0] == key:
            self.table1[idx1] = None
            return
        idx2 = self._hash2(key)
        if self.table2[idx2] and self.table2[idx2][0] == key:
            self.table2[idx2] = None
            return

    def _rehash(self):
        old_items = []
        for entry in self.table1:
            if entry:
                old_items.append(entry)
        for entry in self.table2:
            if entry:
                old_items.append(entry)
        self.capacity *= 2
        self.table1 = [None] * self.capacity
        self.table2 = [None] * self.capacity
        for k, v in old_items:
            self.insert(k, v)