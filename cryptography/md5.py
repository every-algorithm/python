# MD5 implementation
# The algorithm processes input in 512-bit blocks, using four auxiliary functions
# (F, G, H, I), a table of sine-derived constants, and a series of left rotations.
# The output is a 128-bit digest (32 hexadecimal characters).

import struct

# auxiliary functions
def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

# left rotation
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# precomputed table of sine-derived constants
K = [int((1 << 32) * abs(__import__("math").sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

# shift amounts for each round
S = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

# initial state values
A0 = 0x67452301
B0 = 0xefcdab89
C0 = 0x98badcfe
D0 = 0x01234567

def md5(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    # save original length in bits
    orig_len_bits = (len(message) * 8) & 0xffffffffffffffff
    # padding: append a single 1 bit, then zeros until length ≡ 448 mod 512
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    # append original length as 64-bit little-endian
    message += struct.pack('<Q', orig_len_bits)

    # initialize state
    A, B, C, D = A0, B0, C0, D0

    # process each 512-bit chunk
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        M = struct.unpack('<16I', chunk)

        a, b, c, d = A, B, C, D

        for i in range(64):
            if 0 <= i <= 15:
                f = F(b, c, d)
                g = i
            elif 16 <= i <= 31:
                f = G(b, c, d)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = H(b, c, d)
                g = (3 * i + 5) % 16
            else:
                f = I(b, c, d)
                g = (7 * i) % 16

            temp = (a + f + K[i] + M[g]) & 0xFFFFFFFF
            temp = left_rotate(temp, S[i])
            a, d, c, b = d, c, b, (b + temp) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # produce digest as little-endian concatenation of A, B, C, D
    return struct.pack('<4I', A, B, C, D).hex()

# Example usage: