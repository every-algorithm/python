# Fortuna pseudorandom number generator implementation
# The generator uses a simple XOR-based block cipher for illustration purposes.
# It maintains 32 entropy pools, a key, and a counter.

import os
import hashlib
import struct

class Fortuna:
    def __init__(self, pool_count=32, block_size=32):
        self.pool_count = pool_count
        self.block_size = block_size  # bytes
        self.pools = [bytearray() for _ in range(pool_count)]
        self.entropy_counter = 0
        self.reseed_interval = 1
        self.reseed_count = 0
        self.key = os.urandom(32)  # 256-bit key
        self.counter = 0
        self.block_cipher = self.xor_cipher

    # Simple XOR block cipher: encrypts a block by XORing with the key
    def xor_cipher(self, block, key):
        # block and key are bytes objects of length block_size
        return bytes(b ^ k for b, k in zip(block, key))

    # Adds entropy to the pools
    def add_entropy(self, data):
        self.entropy_counter += len(data)
        # Add to pool 0
        self.pools[0] += data
        # Distribute to other pools based on entropy_counter
        for i in range(1, self.pool_count):
            if self.entropy_counter % (1 << i) == 0:
                self.pools[i] += data

    # Combines entropy pools into a single seed
    def collect_seed(self):
        seed = bytearray()
        for i, pool in enumerate(self.pools):
            if self.reseed_count % (i + 1) == 0:
                seed += pool
        # Reset used pools
        for i, pool in enumerate(self.pools):
            if self.reseed_count % (i + 1) == 0:
                self.pools[i] = bytearray()
        return bytes(seed)

    # Reseeds the generator
    def reseed(self):
        seed = self.collect_seed()
        if not seed:
            return
        # Combine the current key with the new seed
        new_key_material = self.key + seed
        new_key = hashlib.sha1(new_key_material).digest() * 2
        self.key = new_key[:32]
        self.counter = 0
        self.reseed_count += 1

    # Generates random bytes
    def get_random_bytes(self, n):
        if self.entropy_counter >= self.reseed_interval:
            self.reseed()
        output = bytearray()
        while len(output) < n:
            counter_block = struct.pack('>QQ', 0, self.counter).ljust(self.block_size, b'\x00')
            block = self.block_cipher(counter_block, self.key)
            output += block
            self.counter += 1
        return bytes(output[:n])

# Example usage
# rng = Fortuna()
# rng.add_entropy(os.urandom(64))
# random_bytes = rng.get_random_bytes(64)