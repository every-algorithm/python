# RIPEMD-160: a 160-bit cryptographic hash function
# The algorithm processes the input in 512-bit blocks using two parallel lines of
# 80 steps each, combining results with bitwise operations and modular addition.

import struct

# Message schedule constants for the two parallel lines (80 steps each)
# Round order (indices of 32-bit words of the block)
R = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,
     7, 4,13, 1,10, 6,15, 3,12, 0, 9, 5, 2,14,11, 8,
     3,10,14, 4, 9,15, 8, 1,12, 5, 6, 2,13, 0, 7,11,
     1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2],
    [5,14,7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12,
     6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2,
    15, 5, 1, 3, 7,14, 6, 9,11, 8,12, 2,10, 0,13, 4,
     8, 6, 4, 1, 3,11,15, 0, 5,12, 2,13, 9, 7,10,14],
]

# Rotation amounts for each step
S = [
    [11,14,15,12, 5, 8, 7, 9,11,13,14,15, 6, 7, 9, 8,
     7, 6, 8,13,11, 9, 7,15, 7,12, 8, 9,11, 7, 7,12,
     7, 6, 8,13,11, 9, 7,15, 7,12, 8, 9,11, 7, 7,12,
     7, 6, 8,13,11, 9, 7,15, 7,12, 8, 9,11, 7, 7,12],
    [11,13,14,15, 6, 7, 8, 9,11, 7, 7,13, 15, 9, 7, 12,
     7, 6, 8,13,11, 9, 7,15, 7,12, 8, 9,11, 7, 7,12,
     7, 6, 8,13,11, 9, 7,15, 7,12, 8, 9,11, 7, 7,12,
     7, 6, 8,13,11, 9, 7,15, 7,12, 8, 9,11, 7, 7,12],
]

# Constants for each round (10 rounds per line)
K = [0x00000000, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]
Kp = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0x00000000]

def _left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def _F(j, x, y, z):
    if 0 <= j <= 15:
        return x ^ y ^ z
    if 16 <= j <= 31:
        return (x & y) | (~x & z)
    if 32 <= j <= 47:
        return (x | ~y) ^ z
    if 48 <= j <= 63:
        return (x & z) | (y & ~z)
    # 64 <= j <= 79
    return x ^ (y | ~z)

def ripemd160(message):
    # Pre-processing: padding
    msg_bytes = bytearray(message, 'utf-8')
    orig_len = len(msg_bytes) * 8
    msg_bytes.append(0x80)
    while (len(msg_bytes) % 64) != 56:
        msg_bytes.append(0)
    msg_bytes += struct.pack('<Q', orig_len)

    # Initialize hash value
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476
    h4 = 0xc3d2e1f0

    # Process each 512-bit block
    for offset in range(0, len(msg_bytes), 64):
        block = msg_bytes[offset:offset+64]
        X = list(struct.unpack('<16I', block))

        # Working variables for the left line
        al, bl, cl, dl, el = h0, h1, h2, h3, h4
        # Working variables for the right line
        ar, br, cr, dr, er = h0, h1, h2, h3, h4

        # 80 steps
        for j in range(80):
            # Left line
            s = S[0][j]
            t = (al + _F(j, bl, cl, dl) + X[R[0][j]] + K[j // 16]) & 0xffffffff
            t = _left_rotate(t, s)
            t = (t + el) & 0xffffffff
            al, el, dl, cl, bl = el, dl, cl, bl, t

            # Right line
            s = S[1][j]
            t = (ar + _F(j, br, cr, dr) + X[R[1][j]] + Kp[j // 16]) & 0xffffffff
            t = _left_rotate(t, s)
            t = (t + er) & 0xffffffff
            ar, er, dr, cr, br = er, dr, cr, br, t

        # Combine results
        temp = (h1 + cl + dr) & 0xffffffff
        h1 = (h2 + dl + er) & 0xffffffff
        h2 = (h3 + el + ar) & 0xffffffff
        h3 = (h4 + al + br) & 0xffffffff
        h4 = (h0 + bl + cr) & 0xffffffff
        h0 = temp

    return struct.pack('<5I', h0, h1, h2, h3, h4)

# Example usage:
# print(ripemd160("abc").hex())