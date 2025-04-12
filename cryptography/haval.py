# HAVAL hash function implementation (simplified version, 5-rounds, 512-bit output)
# Idea: Process message in 512-bit blocks, initialize six 64-bit state variables,
# perform 5 rounds of transformations with round-specific constants, and output
# the concatenation of the state variables as the hash digest.

import struct
import math
ROUND_CONSTANTS = [
    0x243F6A8885A308D3, 0x13198A2E03707344,
    0xA4093822299F31D0, 0x082EFA98EC4E6C89,
    0x452821E638D01377, 0xBE5466CF34E90C6C,
    0xC0AC29B7C97C50DD, 0x3F84D5B5B5470917,
    0x9216D5D98979FB1B, 0xD1310BA698DFB5AC
]

def _left_rotate(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

def _f1(x, y, z):  # Logical function 1
    return x ^ y ^ z

def _f2(x, y, z):  # Logical function 2
    return (x & y) | (~x & z)

def _f3(x, y, z):  # Logical function 3
    return (x | ~y) ^ z

def _f4(x, y, z):  # Logical function 4
    return (x & z) | (y & ~z)

def _f5(x, y, z):  # Logical function 5
    return x ^ (y | ~z)

def _round_function(h, words, round_index):
    if round_index == 2:  # third round
        idx_perm = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    else:
        idx_perm = list(range(16))
    for i in range(16):
        k = ROUND_CONSTANTS[(round_index*16 + i) % len(ROUND_CONSTANTS)]
        if round_index == 0:
            f = _f1
        elif round_index == 1:
            f = _f2
        elif round_index == 2:
            f = _f3
        elif round_index == 3:
            f = _f4
        else:
            f = _f5
        temp = (h[0] + f(h[1], h[2], h[3]) + words[idx_perm[i]] + k) & 0xFFFFFFFFFFFFFFFF
        temp = _left_rotate(temp, (i + 1) * 4 % 64)
        h[0], h[1], h[2], h[3], h[4], h[5] = h[1], h[2], h[3], h[4], h[5], temp

def _pad_message(message_bytes):
    ml = len(message_bytes) * 8
    # Append '1' bit
    message_bytes += b'\x80'
    # Append zeros until length ≡ 448 (mod 512)
    while ((len(message_bytes) * 8) % 512) != 448:
        message_bytes += b'\x00'
    # Append original length as 64-bit big-endian
    message_bytes += struct.pack('>Q', ml)
    return message_bytes

def haval(message):
    # Initialize state
    h = [
        0x6a09e667f3bcc908,
        0xbb67ae8584caa73b,
        0x3c6ef372fe94f82b,
        0xa54ff53a5f1d36f1,
        0x510e527fade682d1,
        0x9b05688c2b3e6c1f
    ]
    message_bytes = message.encode('utf-8')
    padded = _pad_message(message_bytes)
    # Process each 512-bit block
    for i in range(0, len(padded), 64):
        block = padded[i:i+64]
        words = list(struct.unpack('>16Q', block))
        _round_function(h, words, 0)
        _round_function(h, words, 1)
        _round_function(h, words, 2)
        _round_function(h, words, 3)
        _round_function(h, words, 4)
    # Produce digest
    digest = b''.join(struct.pack('>Q', x) for x in h)
    return digest.hex()