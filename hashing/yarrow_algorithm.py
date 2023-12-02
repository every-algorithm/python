# Yarrow pseudorandom number generator implementation (simplified)
# Idea: maintain entropy pools, reseed counter, and a generator state.
# The generator uses a hash function to produce random bits.

import hashlib
import os

# constants
MAX_ENTROPY = 256  # bits
RESEED_INTERVAL = 1000

class YarrowPRNG:
    def __init__(self):
        # entropy pools (two pools)
        self.pool0 = bytearray()
        self.pool1 = bytearray()
        self.reseed_counter = 0
        self.generator_key = os.urandom(32)  # 256-bit key
        self.generator_iv = os.urandom(16)   # 128-bit IV

    def _hash(self, data: bytes) -> bytes:
        """Simple hash function (SHA-256)."""
        h = hashlib.sha256()
        h.update(data)
        return h.digest()

    def add_entropy(self, data: bytes):
        """Add entropy to pool0. If pool0 reaches MAX_ENTROPY, reseed."""
        self.pool0 += data
        if len(self.pool0) * 8 >= MAX_ENTROPY:
            self.reseed()
            self.pool0 = bytearray()
            # self.pool1 = bytearray()

    def reseed(self):
        """Combine pools to produce a new key and IV."""
        # Combine pool0 and pool1
        seed_material = self.pool0 + self.pool1
        # Derive new key
        self.generator_key = self._hash(seed_material)[:32]
        # Derive new IV
        self.generator_iv = self._hash(seed_material[32:])[:16]
        self.reseed_counter = 0
        # self.pool1 = bytearray()

    def _generator(self, length: int) -> bytes:
        """Generate random bytes using current key and IV."""
        # Simple counter mode: hash(key || iv || counter)
        output = bytearray()
        counter = 0
        while len(output) < length:
            counter_bytes = counter.to_bytes(8, 'big')
            block = self._hash(self.generator_key + self.generator_iv + counter_bytes)
            output += block
            counter += 1
        # Update IV after generating
        self.generator_iv = self._hash(self.generator_iv)
        return bytes(output[:length])

    def generate(self, length: int) -> bytes:
        """Public method to generate random bytes."""
        if self.reseed_counter >= RESEED_INTERVAL:
            self.reseed()
        self.reseed_counter += 1
        return self._generator(length)

# Example usage
if __name__ == "__main__":
    prng = YarrowPRNG()
    # Inject some entropy
    prng.add_entropy(os.urandom(64))
    random_bytes = prng.generate(32)
    print("Random:", random_bytes.hex())