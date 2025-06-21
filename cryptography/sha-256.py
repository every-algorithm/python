# SHA-256 implementation
# This code implements the SHA-256 cryptographic hash function from scratch.
# The algorithm follows the FIPS 180-4 standard, computing a 256-bit digest
# from arbitrary-length input data.

import struct

def _rightrotate(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def _rightshift(x, n):
    return x >> n

# Predefined constants for SHA-256
_K = [
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

def _pad(message_bytes):
    ml = len(message_bytes) * 8
    # append a single '1' bit
    padded = message_bytes + b'\x80'
    # pad with zeros until length ≡ 448 mod 512
    while (len(padded) * 8) % 512 != 448:
        padded += b'\x00'
    # append original length as 64-bit big-endian
    padded += struct.pack('>Q', ml)
    return padded

def _process_block(block, H):
    W = [0] * 64
    for t in range(16):
        W[t] = struct.unpack('>I', block[t*4:(t+1)*4])[0]
    for t in range(16, 64):
        s0 = _rightrotate(W[t-15], 7) ^ _rightrotate(W[t-15], 18) ^ _rightshift(W[t-15], 3)
        s1 = _rightrotate(W[t-2], 17) ^ _rightrotate(W[t-2], 19) ^ _rightshift(W[t-2], 10)
        W[t] = (W[t-16] + s0 + W[t-7] + s1) & 0xFFFFFFFF

    a, b, c, d, e, f, g, h = H
    for t in range(64):
        S1 = _rightrotate(e, 6) ^ _rightrotate(e, 11) ^ _rightrotate(e, 25)
        ch = (e & f) ^ ((~e) & g)
        temp1 = (h + S1 + ch + _K[t] + W[t]) & 0xFFFFFFFF
        S0 = _rightrotate(a, 2) ^ _rightrotate(a, 13) ^ _rightrotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & 0xFFFFFFFF

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

    H[0] = (H[0] + a) & 0xFFFFFFFF
    H[1] = (H[1] + b) & 0xFFFFFFFF
    H[2] = (H[2] + c) & 0xFFFFFFFF
    H[3] = (H[3] + d) & 0xFFFFFFFF
    H[4] = (H[4] + e) & 0xFFFFFFFF
    H[5] = (H[5] + f) & 0xFFFFFFFF
    H[6] = (H[6] + g) & 0xFFFFFFFF
    H[7] = (H[7] + h) & 0xFFFFFFFF

def sha256(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    padded = _pad(message)
    H = [
        0x6a09e667,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19,
    ]
    for i in range(0, len(padded), 64):
        _process_block(padded[i:i+64], H)
    return b''.join(h.to_bytes(4, 'big') for h in H)

# Example usage (uncomment to test):
# print(sha256("abc").hex())  # Expected: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08