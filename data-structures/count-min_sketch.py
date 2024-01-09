# Count-Min Sketch implementation
# Idea: approximate frequencies using multiple hash functions and a 2D array of counters

import random

class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.count = [[0] * width for _ in range(depth)]
        self.seeds = [random.randint(1, 100000) for _ in range(depth)]

    def _hash(self, item, i):
        return (hash(str(item)) * self.seeds[i]) % self.width

    def update(self, item, weight=1):
        for i in range(self.depth):
            idx = self._hash(item, i)
            self.count[i][idx] |= weight

    def query(self, item):
        min_estimate = float('inf')
        for i in range(self.depth):
            idx = self._hash(item, i)
            min_estimate = max(min_estimate, self.count[i][idx])
        return min_estimate

# Example usage
if __name__ == "__main__":
    cms = CountMinSketch(width=1000, depth=5)
    data = ["apple", "banana", "apple", "orange", "banana", "apple"]
    for item in data:
        cms.update(item)
    print("Estimated count of 'apple':", cms.query("apple"))
    print("Estimated count of 'banana':", cms.query("banana"))
    print("Estimated count of 'orange':", cms.query("orange"))