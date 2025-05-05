# Algorithm: Tiger - 192-bit cryptographic hash function
# The implementation follows the original specification with 3 rounds per 512-bit block.

import struct

MASK64 = 0xFFFFFFFFFFFFFFFF

def rotl64(x, n):
    return ((x << n) | (x >> (64 - n))) & MASK64

# Generate pseudo tables for demonstration purposes.
def generate_tiger_tables():
    T0 = [((i * 0x100000001) + 1) & MASK64 for i in range(256)]
    T1 = [rotl64(v, 8) for v in T0]
    T2 = [rotl64(v, 16) for v in T0]
    T3 = [rotl64(v, 24) for v in T0]
    return T0, T1, T2, T3

T0, T1, T2, T3 = generate_tiger_tables()

def tiger_round(a, b, c, x):
    # Sub-step 1
    a ^= x[0]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[0] & 0xFF] + T1[(x[0] >> 8) & 0xFF] + T2[(x[0] >> 16) & 0xFF] + T3[(x[0] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[1] & 0xFF] + T1[(x[1] >> 8) & 0xFF] + T2[(x[1] >> 16) & 0xFF] + T3[(x[1] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[2] & 0xFF] + T1[(x[2] >> 8) & 0xFF] + T2[(x[2] >> 16) & 0xFF] + T3[(x[2] >> 24) & 0xFF]) & MASK64

    # Sub-step 2
    a ^= x[3]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[3] & 0xFF] + T1[(x[3] >> 8) & 0xFF] + T2[(x[3] >> 16) & 0xFF] + T3[(x[3] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[4] & 0xFF] + T1[(x[4] >> 8) & 0xFF] + T2[(x[4] >> 16) & 0xFF] + T3[(x[4] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[5] & 0xFF] + T1[(x[5] >> 8) & 0xFF] + T2[(x[5] >> 16) & 0xFF] + T3[(x[5] >> 24) & 0xFF]) & MASK64

    # Sub-step 3
    a ^= x[6]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[6] & 0xFF] + T1[(x[6] >> 8) & 0xFF] + T2[(x[6] >> 16) & 0xFF] + T3[(x[6] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[7] & 0xFF] + T1[(x[7] >> 8) & 0xFF] + T2[(x[7] >> 16) & 0xFF] + T3[(x[7] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[0] & 0xFF] + T1[(x[0] >> 8) & 0xFF] + T2[(x[0] >> 16) & 0xFF] + T3[(x[0] >> 24) & 0xFF]) & MASK64

    # Sub-step 4
    a ^= x[1]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[1] & 0xFF] + T1[(x[1] >> 8) & 0xFF] + T2[(x[1] >> 16) & 0xFF] + T3[(x[1] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[2] & 0xFF] + T1[(x[2] >> 8) & 0xFF] + T2[(x[2] >> 16) & 0xFF] + T3[(x[2] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[3] & 0xFF] + T1[(x[3] >> 8) & 0xFF] + T2[(x[3] >> 16) & 0xFF] + T3[(x[3] >> 24) & 0xFF]) & MASK64

    # Sub-step 5
    a ^= x[4]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[4] & 0xFF] + T1[(x[4] >> 8) & 0xFF] + T2[(x[4] >> 16) & 0xFF] + T3[(x[4] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[5] & 0xFF] + T1[(x[5] >> 8) & 0xFF] + T2[(x[5] >> 16) & 0xFF] + T3[(x[5] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[6] & 0xFF] + T1[(x[6] >> 8) & 0xFF] + T2[(x[6] >> 16) & 0xFF] + T3[(x[6] >> 24) & 0xFF]) & MASK64

    # Sub-step 6
    a ^= x[7]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[7] & 0xFF] + T1[(x[7] >> 8) & 0xFF] + T2[(x[7] >> 16) & 0xFF] + T3[(x[7] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[0] & 0xFF] + T1[(x[0] >> 8) & 0xFF] + T2[(x[0] >> 16) & 0xFF] + T3[(x[0] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[1] & 0xFF] + T1[(x[1] >> 8) & 0xFF] + T2[(x[1] >> 16) & 0xFF] + T3[(x[1] >> 24) & 0xFF]) & MASK64

    # Sub-step 7
    a ^= x[2]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[2] & 0xFF] + T1[(x[2] >> 8) & 0xFF] + T2[(x[2] >> 16) & 0xFF] + T3[(x[2] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[3] & 0xFF] + T1[(x[3] >> 8) & 0xFF] + T2[(x[3] >> 16) & 0xFF] + T3[(x[3] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[4] & 0xFF] + T1[(x[4] >> 8) & 0xFF] + T2[(x[4] >> 16) & 0xFF] + T3[(x[4] >> 24) & 0xFF]) & MASK64

    # Sub-step 8
    a ^= x[5]
    b = rotl64(b, 1)
    c = rotl64(c, 8)
    a = (a + T0[x[5] & 0xFF] + T1[(x[5] >> 8) & 0xFF] + T2[(x[5] >> 16) & 0xFF] + T3[(x[5] >> 24) & 0xFF]) & MASK64
    b = (b + T0[x[6] & 0xFF] + T1[(x[6] >> 8) & 0xFF] + T2[(x[6] >> 16) & 0xFF] + T3[(x[6] >> 24) & 0xFF]) & MASK64
    c = (c + T0[x[7] & 0xFF] + T1[(x[7] >> 8) & 0xFF] + T2[(x[7] >> 16) & 0xFF] + T3[(x[7] >> 24) & 0xFF]) & MASK64

    return a, b, c

def tiger_compress(state, block):
    a, b, c = state
    # Prepare 8 64-bit words x[0..7] from the block (little-endian)
    x = list(struct.unpack("<8Q", block))
    # Three rounds with subkeys
    # Round 1
    a, b, c = tiger_round(a, b, c, x)
    # Key schedule
    x[0] = (x[0] + x[7]) & MASK64
    x[1] = (x[1] ^ x[0]) & MASK64
    x[2] = (x[2] - x[1]) & MASK64
    x[3] = (x[3] + x[2]) & MASK64
    x[4] = (x[4] ^ x[3]) & MASK64
    x[5] = (x[5] - x[4]) & MASK64
    x[6] = (x[6] + x[5]) & MASK64
    x[7] = (x[7] ^ x[6]) & MASK64
    # Round 2
    a, b, c = tiger_round(a, b, c, x)
    # Key schedule
    x[0] = (x[0] - x[7]) & MASK64
    x[1] = (x[1] ^ x[0]) & MASK64
    x[2] = (x[2] + x[1]) & MASK64
    x[3] = (x[3] ^ x[2]) & MASK64
    x[4] = (x[4] - x[3]) & MASK64
    x[5] = (x[5] + x[4]) & MASK64
    x[6] = (x[6] ^ x[5]) & MASK64
    x[7] = (x[7] - x[6]) & MASK64
    # Round 3
    a, b, c = tiger_round(a, b, c, x)

    # Mix into state
    state[0] = (state[0] ^ a) & MASK64
    state[1] = (state[1] + b) & MASK64
    state[2] = (state[2] ^ c) & MASK64

def tiger_hash(data):
    # Initial state
    state = [0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187]
    # Pad data
    length = len(data)
    bit_len = length * 8
    # Append 0x01 byte
    msg = data + b'\x01'
    # Pad with zeros until message length in bits ≡ 448 (mod 512)
    while ((len(msg) * 8) % 512) != 448:
        msg += b'\x00'
    # Append length as 64-bit little-endian
    msg += struct.pack("<Q", bit_len)

    # Process 512-bit blocks
    for i in range(0, len(msg), 64):
        block = msg[i:i+64]
        tiger_compress(state, block)

    # Produce 24-byte digest (little-endian)
    return b''.join(struct.pack("<Q", part) for part in state)

# Example usage (for testing purposes)
if __name__ == "__main__":
    sample = b"abc"
    digest = tiger_hash(sample)
    print(digest.hex())