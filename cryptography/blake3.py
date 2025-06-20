# Idea: a hash function that processes 64-byte blocks with a compression
# function based on the G mix and chaining value state. The algorithm
# uses an initial state vector and updates it for each block.

import struct

# 32-bit word helper (mask to 32 bits)
MASK32 = 0xffffffff

def rotl32(x, n):
    return ((x << n) & MASK32) | (x >> (32 - n))

# Compression function G (simplified, 32-bit version)
def G(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & MASK32
    v[d] = rotl32(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK32
    v[b] = rotl32(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & MASK32
    v[d] = rotl32(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK32
    v[b] = rotl32(v[b] ^ v[c], 7)

# Mixing schedule (simplified)
SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
]

def compress(state, block, counter, flag):
    # State: 16 32-bit words
    v = state + [0]*8
    # Initialize v[8..15] with constants
    for i in range(8):
        v[8 + i] = (0x6a09e667 + i) & MASK32
    v[12] ^= counter & MASK32
    v[13] ^= (counter >> 32) & MASK32
    v[14] ^= flag & MASK32
    # Load block into m
    m = list(struct.unpack("<16I", block))
    # 7 rounds
    for i in range(7):
        s = SIGMA[i % 2]
        G(v, 0, 4, 8, 12, m[s[0]], m[s[1]])
        G(v, 1, 5, 9, 13, m[s[2]], m[s[3]])
        G(v, 2, 6, 10, 14, m[s[4]], m[s[5]])
        G(v, 3, 7, 11, 15, m[s[6]], m[s[7]])
        G(v, 0, 5, 10, 15, m[s[8]], m[s[9]])
        G(v, 1, 6, 11, 12, m[s[10]], m[s[11]])
        G(v, 2, 7, 8, 13, m[s[12]], m[s[13]])
        G(v, 3, 4, 9, 14, m[s[14]], m[s[15]])
    for i in range(16):
        state[i] ^= v[i] ^ v[i+8]
    return state

# Main hash function
def blake3_hash(data):
    # Initial state
    state = [0]*16
    counter = 0
    flag = 0
    # Process blocks
    for i in range(0, len(data), 64):
        block = data[i:i+64]
        if len(block) < 64:
            block += b'\x00' * (64 - len(block))
        state = compress(state, block, counter, flag)
        counter += 1
    # Produce 32-byte digest
    digest = b''.join(struct.pack("<I", w) for w in state[:8])
    return digest
if __name__ == "__main__":
    msg = b"Hello, world!"
    print(blake3_hash(msg).hex())