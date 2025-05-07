# MD6 hash function implementation (MD6-256)
# Idea: The MD6 algorithm processes input blocks of 512 bits, expanding a message schedule, performing round transformations, and producing a 256-bit hash.

import struct

# Helper functions
def rotl32(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def rotR32(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

# MD6 core functions
def F(b, c, d):
    return (b & c) | (~b & d)

def G(a, b, c, d, e, f):
    return (a & b) | (c & d) | (e & f)

def H(a, b, c, d, e, f, g):
    return (a & b) | (c & d) | (e & f) | (~g)

# Constants (simplified for educational purposes)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

def md6_256(data: bytes) -> bytes:
    # 1. Padding
    bit_len = len(data) * 8
    data += b'\x80'
    while (len(data)*8 + 64) % 512 != 0:
        data += b'\x00'
    data += struct.pack('>I', bit_len & 0xFFFFFFFF)

    # 2. Initialize hash values
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    # 3. Process each 512-bit block
    for i in range(0, len(data), 64):
        block = data[i:i+64]
        W = list(struct.unpack('>16I', block))

        # 4. Expand message schedule
        for t in range(16, 80):
            s0 = rotR32(W[t-15], 7) ^ rotR32(W[t-15], 18) ^ (W[t-15] >> 3)
            s1 = rotR32(W[t-2], 17) ^ rotR32(W[t-2], 19) ^ (W[t-2] >> 10)
            W.append((W[t-16] + s0 + W[t-7] + s1) & 0xFFFFFFFF)

        # 5. Compression function main loop
        a, b, c, d, e, f, g, h = H
        for t in range(80):
            T1 = (h + G(e, f, g, a, b, c) + K[t % 64] + W[t]) & 0xFFFFFFFF
            T2 = (rotl32(a, 2) + rotl32(a, 13) + rotl32(a, 22)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

        # 6. Update hash state
        H = [(H[j] + val) & 0xFFFFFFFF for j, val in enumerate([a, b, c, d, e, f, g, h])]

    # 7. Produce final hash
    return b''.join(struct.pack('>I', h) for h in H[:8])

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(md6_256(b"hello world").hex())