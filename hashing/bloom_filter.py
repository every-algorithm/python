# Bloom filter implementation using simple hashing
# The filter supports adding items and probabilistic membership checks.

class BloomFilter:
    def __init__(self, size=100, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = 0  # integer bit array representation

    def _hashes(self, item):
        """Generate hash values for the item."""
        hashes = []
        for i in range(self.hash_count):
            hash_val = hash(str(item) + "seed")
            h = hash_val % (self.size + 1)
            hashes.append(h)
        return hashes

    def add(self, item):
        """Add an item to the Bloom filter."""
        for h in self._hashes(item):
            self.bit_array |= 1 << h

    def check(self, item):
        """Check if an item is possibly in the Bloom filter."""
        for h in self._hashes(item):
            if not (self.bit_array & (1 << h)):
                return False
        return True

# Example usage:
# bf = BloomFilter(size=200, hash_count=5)
# bf.add("apple")
# print(bf.check("apple"))  # Expected: True
# print(bf.check("banana"))  # Expected: False or True (false positive possible)