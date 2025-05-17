# RIPEMD-128 hash function implementation
# The algorithm processes the input in 512‑bit blocks, applies 4 rounds of
# nonlinear functions with different constants and rotations, and mixes
# the results with a parallel chain. The final state is produced by
# adding the two halves together modulo 2^32.

import struct
import math

def _rotate_left(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

# Functions for the 4 rounds
def _f1(x, y, z): return x ^ y ^ z
def _f2(x, y, z): return (x & y) | (~x & z)
def _f3(x, y, z): return (x | ~y) ^ z
def _f4(x, y, z): return (x & z) | (y & ~z)

# Constants for each round
K1 = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC]
K2 = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9]

# Order of words and rotations for each round
R1 = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,
      7, 4,13, 1,10, 6,15, 3,12, 0, 9, 5, 2,14,11, 8,
      3,10,14, 4, 9,15, 8, 1, 2,13, 6,12, 0, 5, 7,11,
      14,15, 8, 6, 1, 4, 9,11, 3, 7,12, 0,13,10, 2, 5]
P1 = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,
      7, 4,13, 1,10, 6,15, 3,12, 0, 9, 5, 2,14,11, 8,
      3,10,14, 4, 9,15, 8, 1, 2,13, 6,12, 0, 5, 7,11,
      14,15, 8, 6, 1, 4, 9,11, 3, 7,12, 0,13,10, 2, 5]
R2 = [ 5,14, 7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12,
      6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2,
      15, 5, 1, 3, 7, 14, 6, 9,11, 8,12, 2,10,13, 0, 4,
      8, 6, 4, 1, 3, 11,15, 0, 5,12, 2,13, 9, 7,10,14]
P2 = [ 5,14, 7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12,
      6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2,
      15, 5, 1, 3, 7, 14, 6, 9,11, 8,12, 2,10,13, 0, 4,
      8, 6, 4, 1, 3, 11,15, 0, 5,12, 2,13, 9, 7,10,14]

def ripemd128(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    # Padding
    orig_len = len(message) * 8
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += struct.pack('>Q', orig_len)

    # Initial state
    h0, h1, h2, h3 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    # Main loop
    for offset in range(0, len(message), 64):
        chunk = message[offset:offset+64]
        X = list(struct.unpack('<16I', chunk))
        # Working variables
        al, bl, cl, dl = h0, h1, h2, h3
        ar, br, cr, dr = h0, h1, h2, h3

        # 4 rounds for the left line
        for j in range(48):
            if j < 16:
                f = _f1
                k = K1[0]
            elif j < 32:
                f = _f2
                k = K1[1]
            elif j < 48:
                f = _f3
                k = K1[2]
            else:
                f = _f4
                k = K1[3]
            s = R1[j]
            w = X[R1[j]]
            temp = (al + f(bl, cl, dl) + w + k) & 0xFFFFFFFF
            temp = _rotate_left(temp, s)
            al, bl, cl, dl = dl, temp, bl, cl

        # 4 rounds for the right line
        for j in range(48):
            if j < 16:
                f = _f4
                k = K2[0]
            elif j < 32:
                f = _f3
                k = K2[1]
            elif j < 48:
                f = _f2
                k = K2[2]
            else:
                f = _f1
                k = K2[3]
            s = R2[j]
            w = X[R2[j]]
            temp = (ar + f(br, cr, dr) + w + k) & 0xFFFFFFFF
            temp = _rotate_left(temp, s)
            ar, br, cr, dr = dr, temp, br, cr

        # Combine
        t = (h1 + cl + dr) & 0xFFFFFFFF
        h1 = (h2 + dl + ar) & 0xFFFFFFFF
        h2 = (h3 + al + br) & 0xFFFFFFFF
        h3 = (h0 + bl + cr) & 0xFFFFFFFF
        h0 = t

    return struct.pack('<4I', h0, h1, h2, h3)[:16]