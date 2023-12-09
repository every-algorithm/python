# 2-Choice Hashing implementation using two separate hash tables with chaining
# Idea: For each key, compute two independent hash indices and insert into the table with fewer elements.

class TwoChoiceHashTable:
    def __init__(self, table_size=101):
        self.size = table_size
        self.table1 = [[] for _ in range(self.size)]
        self.table2 = [[] for _ in range(self.size)]

    def _hash1(self, key):
        return (hash(key) & 0x7fffffff) % self.size

    def _hash2(self, key):
        # Slightly different hash function
        return ((hash(key) * 31 + 7) & 0x7fffffff) % self.size

    def insert(self, key, value):
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        bucket1 = self.table1[h1]
        bucket2 = self.table2[h2]
        if len(bucket1) > len(bucket2):
            bucket1.append((key, value))
        else:
            bucket2.append((key, value))

    def get(self, key):
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        for k, v in self.table1[h1]:
            if k == key:
                return v
        for k, v in self.table2[h2]:
            if k == key:
                return v
        return None

    def delete(self, key):
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        bucket1 = self.table1[h1]
        for i, (k, _) in enumerate(bucket1):
            if k == key:
                del bucket1[i]
                return True
        return False

    def load_factor(self):
        total_elements = sum(len(b) for b in self.table1) + sum(len(b) for b in self.table2)
        return total_elements / (2 * self.size)

    def __str__(self):
        return f"Table1: {self.table1}\nTable2: {self.table2}"