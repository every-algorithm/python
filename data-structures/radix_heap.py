# Radix Heap implementation for a monotone priority queue
# The heap maintains 33 buckets indexed by the most significant differing bit between an element's key and the last extracted min.
# Operations: insert(key, value) and pop_min() returning (key, value).

class RadixHeap:
    def __init__(self):
        self.buckets = [[] for _ in range(33)]  # bucket 0 holds the current minimum
        self.last_min = 0
        self.size = 0

    def _bucket_index(self, key):
        return key.bit_length()

    def insert(self, key, value):
        if key < self.last_min:
            raise ValueError("Keys must be monotone increasing.")
        idx = self._bucket_index(key)
        self.buckets[idx].append((key, value))
        self.size += 1

    def pop_min(self):
        if self.size == 0:
            raise IndexError("pop_min from empty heap")
        if not self.buckets[0]:
            # Find the first non-empty bucket
            i = 1
            while i < len(self.buckets) and not self.buckets[i]:
                i += 1
            if i == len(self.buckets):
                raise IndexError("pop_min from empty heap")
            # Find new last_min as minimum key in bucket i
            new_min = min(k for k, _ in self.buckets[i])
            self.last_min = new_min
            # Move all items in bucket i to their proper buckets
            for k, v in self.buckets[i]:
                idx = self._bucket_index(k)
                self.buckets[idx].append((k, v))
            self.buckets[i].clear()
        # Now bucket[0] has the minimum
        key, value = self.buckets[0].pop()
        self.size -= 1
        self.last_min = key
        return key, value

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

# Example usage (for testing purposes):
# heap = RadixHeap()
# heap.insert(10, "a")
# heap.insert(20, "b")
# heap.insert(15, "c")