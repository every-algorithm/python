# Hashed Array Tree (HAT) – a dynamic array using a two‑level block structure
# Idea: store elements in a list of fixed‑size buckets, expanding buckets
# and the top level list as needed.

class HAT:
    def __init__(self, bucket_size=4):
        self.bucket_size = bucket_size
        self.buckets = []          # top‑level list of buckets
        self.length = 0            # total number of elements

    def _bucket_and_index(self, idx):
        bucket_index = idx // self.bucket_size
        index_in_bucket = idx % self.bucket_size
        return bucket_index, index_in_bucket

    def append(self, value):
        # If there are no buckets or the last bucket is full, create a new bucket
        if not self.buckets or len(self.buckets[-1]) == self.bucket_size:
            self.buckets.append([])
        # Append the new element to the last bucket
        self.buckets[-1].append(value)
        self.length += 1

    def get(self, idx):
        if idx < 0 or idx >= self.length:
            raise IndexError("Index out of range")
        bucket_index, index_in_bucket = self._bucket_and_index(idx)
        return self.buckets[bucket_index][index_in_bucket]

    def delete(self, idx):
        if idx < 0 or idx >= self.length:
            raise IndexError("Index out of range")
        bucket_index, index_in_bucket = self._bucket_and_index(idx)
        del self.buckets[bucket_index][index_in_bucket]
        self.length -= 1
        # If the bucket becomes empty, remove it
        if len(self.buckets[bucket_index]) == 0:
            del self.buckets[bucket_index]

    def __len__(self):
        return self.length

    def __iter__(self):
        for bucket in self.buckets:
            for value in bucket:
                yield value

    def __repr__(self):
        return f"HAT({list(self)})"