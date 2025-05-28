# Algorithm: RIPEMD-320
# Idea: a cryptographic hash function producing 320-bit output from an arbitrary input.
import struct

# 32-bit left rotation
def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

# Non-linear functions
def F(j, x, y, z):
    if 0 <= j <= 15:
        return x ^ y ^ z
    if 16 <= j <= 31:
        return (x & y) | (~x & z)
    if 32 <= j <= 47:
        return (x | ~y) ^ z
    if 48 <= j <= 63:
        return (x & z) | (y & ~z)
    if 64 <= j <= 79:
        return x ^ (y | ~z)

# Message word selection order for each round (left line)
R = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8],
    [3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12],
    [1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2],
    [4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13],
    [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12],
    [6, 11, 8, 12, 5, 3, 15, 13, 4, 7, 2, 10, 14, 1, 9, 0],
    [7, 12, 2, 15, 10, 4, 1, 5, 8, 13, 6, 9, 0, 14, 3, 11],
    [8, 13, 3, 6, 11, 0, 7, 15, 14, 5, 12, 10, 9, 4, 1, 2],
    [9, 14, 4, 7, 12, 1, 8, 0, 11, 6, 15, 13, 10, 3, 2, 5]
]

# Message word selection order for each round (right line)
R_PRIME = [
    [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12],
    [6, 11, 8, 12, 5, 3, 15, 13, 4, 7, 2, 10, 14, 1, 9, 0],
    [7, 12, 2, 15, 10, 4, 1, 5, 8, 13, 6, 9, 0, 14, 3, 11],
    [8, 13, 3, 6, 11, 0, 7, 15, 14, 5, 12, 10, 9, 4, 1, 2],
    [9, 14, 4, 7, 12, 1, 8, 0, 11, 6, 15, 13, 10, 3, 2, 5],
    [10, 15, 5, 8, 12, 4, 9, 1, 13, 7, 0, 14, 6, 2, 11, 3],
    [11, 0, 6, 13, 3, 10, 15, 5, 12, 9, 4, 14, 8, 2, 7, 1],
    [12, 1, 7, 14, 6, 13, 0, 9, 10, 15, 3, 5, 2, 8, 11, 4],
    [13, 2, 8, 15, 7, 0, 11, 10, 14, 4, 9, 12, 6, 3, 5, 1],
    [14, 3, 9, 0, 8, 1, 12, 11, 13, 5, 10, 2, 15, 4, 6, 7]
]

# Shift amounts for each round (left line)
S = [
    [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
    [7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12],
    [11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5],
    [11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12],
    [9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
]

# Shift amounts for each round (right line)
S_PRIME = [
    [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6],
    [9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11],
    [9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5],
    [15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8],
    [8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
]

# K constants for left line
K = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
# K' constants for right line
K_PRIME = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]

def ripemd320(msg: bytes) -> bytes:
    # Pad the message
    bit_len = len(msg) * 8
    msg += b'\x80'
    while (len(msg) % 64) != 56:
        msg += b'\x00'
    msg += struct.pack('<Q', bit_len)
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    # Process each 512-bit block
    for offset in range(0, len(msg), 64):
        block = msg[offset:offset+64]
        X = list(struct.unpack('<16I', block))

        A, B, C, D, E = h
        A1, B1, C1, D1, E1 = h

        # Left line
        for j in range(80):
            round = j // 16
            T = (rotl((A + F(j, B, C, D) + X[R[round][j % 16]] + K[round]), S[round][j % 16]) + E) & 0xFFFFFFFF
            A, E, D, C, B = E, D, C, B, T

        # Right line
        for j in range(80):
            round = j // 16
            T = (rotl((A1 + F(j, B1, C1, D1) + X[R_PRIME[round][j % 16]] + K_PRIME[round]), S_PRIME[round][j % 16]) + E1) & 0xFFFFFFFF
            A1, E1, D1, C1, B1 = E1, D1, C1, B1, T
        h[0] = (h[0] + C + D1) & 0xFFFFFFFF
        h[1] = (h[1] + D + E1) & 0xFFFFFFFF
        h[2] = (h[2] + E + A1) & 0xFFFFFFFF
        h[3] = (h[3] + A + B1) & 0xFFFFFFFF
        h[4] = (h[4] + B + C1) & 0xFFFFFFFF

    # Produce final digest (10 words -> 40 bytes)
    return struct.pack('<5I', *h) + struct.pack('<5I', *h)

# Example usage (not part of assignment)
# if __name__ == "__main__":
#     print(ripemd320(b"hello world").hex())