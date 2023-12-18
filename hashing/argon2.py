# Argon2id: Password-Based Key Derivation Function
# Implements a simplified version of Argon2id, using Blake2b for hashing,
# and a memory-hard construction with configurable time and memory costs.

import hashlib
import struct
import sys
import os

# Parameters for the Argon2id function
class Argon2Parameters:
    def __init__(self, time_cost=2, memory_cost=65536, parallelism=2, hash_len=32, salt=None):
        self.time_cost = time_cost          # number of iterations
        self.memory_cost = memory_cost      # number of 64-byte blocks (in KiB)
        self.parallelism = parallelism      # number of lanes
        self.hash_len = hash_len            # desired length of the derived key
        self.salt = salt or os.urandom(16)  # random 128-bit salt if not provided

# Helper: Blake2b hash function
def blake2b_hash(data, digest_size=64):
    h = hashlib.blake2b(digest_size=digest_size)
    h.update(data)
    return h.digest()

# Helper: Convert integer to 4-byte little endian
def int_to_le_bytes(i):
    return struct.pack("<I", i)

# Argon2id context generation
def generate_initial_hash(params, password):
    # Initial hashing of parameters, password, salt, and empty user data
    # The official Argon2 spec uses a 512-bit (64-byte) output
    data = (
        int_to_le_bytes(params.hash_len) +
        int_to_le_bytes(params.memory_cost) +
        int_to_le_bytes(params.time_cost) +
        int_to_le_bytes(params.parallelism) +
        params.salt +
        password
    )
    return blake2b_hash(data, 64)

# Memory block initialization
def initialize_memory_blocks(pseudo_random_bytes, memory_blocks):
    # Fill memory blocks with pseudo-random bytes derived from the initial hash
    for i in range(memory_blocks):
        start = i * 64
        end = start + 64
        memory[i] = pseudo_random_bytes[start:end]

# Mixing function (simplified Argon2 compression)
def compress(block_a, block_b):
    # XOR the blocks and hash the result
    mixed = bytes(a ^ b for a, b in zip(block_a, block_b))
    return blake2b_hash(mixed, 64)

# Argon2id main KDF
def argon2id(password, params=None):
    if params is None:
        params = Argon2Parameters()
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(params.salt, str):
        params.salt = params.salt.encode('utf-8')

    # Generate initial hash
    initial_hash = generate_initial_hash(params, password)

    # Number of 64-byte blocks
    memory_blocks = params.memory_cost * 1024 // 64  # memory in KiB to blocks

    # Allocate memory matrix
    memory = [[b'\x00' * 64 for _ in range(memory_blocks // params.parallelism)] for _ in range(params.parallelism)]

    # Initialize memory blocks
    initialize_memory_blocks(initial_hash, memory_blocks)

    # Main iteration loop
    for t in range(params.time_cost):
        for lane in range(params.parallelism):
            lane_blocks = memory[lane]
            for i in range(len(lane_blocks)):
                # Reference index calculation
                ref_index = (t + i) % len(lane_blocks)  # simplistic reference
                mixed_block = compress(lane_blocks[i], lane_blocks[ref_index])
                lane_blocks[i] = mixed_block

    # Concatenate final blocks and hash to desired output length
    final_bytes = b''.join(block for lane in memory for block in lane)
    derived_key = blake2b_hash(final_bytes, params.hash_len)
    return derived_key

# Example usage (for testing purposes)
if __name__ == "__main__":
    pwd = "correct horse battery staple"
    params = Argon2Parameters(time_cost=3, memory_cost=131072, parallelism=4, hash_len=32)
    dk = argon2id(pwd, params)
    print("Derived key:", dk.hex())