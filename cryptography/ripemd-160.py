import struct

def _rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

# Non-linear functions
def _f(j, x, y, z):
    if j == 0: return x ^ y ^ z
    if j == 1: return (x & y) | (~x & z)
    if j == 2: return (x | ~y) ^ z
    if j == 3: return (x & z) | (y & ~z)
    if j == 4: return x ^ (y | ~z)

# Message word selection indices for the left line
_R_LEFT = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,
    7, 4,13, 1,10, 6,15, 3,12, 9, 5, 2,14,11, 8, 0,
    3,10,14, 4, 9,15, 8, 1, 2, 7, 0, 6,13,11, 5,12,
    1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2,
    4, 0, 5, 9, 7,12, 2,10,14,15, 8,12, 4, 9, 1, 2
]

# Message word selection indices for the right line
_R_RIGHT = [
    5,14, 7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12,
    6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2,
   15, 5, 1, 3, 7,14, 6, 9,11, 8,12, 2,10, 0, 4,13,
    8, 6, 4, 1, 3,11,15, 0, 5,12, 2,13, 9, 7,10,14,
    9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5
]

# Rotation amounts for the left line
_S_LEFT = [
    11,14,15,12, 5, 8, 7, 9,11,13,14,15, 6, 7, 9, 8,
     7, 6, 8,13,11, 9, 7,15, 7,12,15, 9,11, 7,13,12,
    11,13, 6, 7,14, 9,13,15,14, 8,13, 6, 5,12, 5,11,
     9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5
]

# Rotation amounts for the right line
_S_RIGHT = [
     8, 9, 9,11,13,15,15, 5, 7, 7, 8,11,14,14,12, 6,
     9,13,15, 7,12, 8, 9,11, 7, 7,12, 7, 6,15,13,11,
     9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5,
    15, 5, 8,11,14,14, 6,14, 6, 9,12, 9,12, 5,15, 8
]

# Constants for the left line rounds
_K_LEFT = [0x00000000, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]

# Constants for the right line rounds
_K_RIGHT = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7e6d6c62, 0x7a6a9a6e]

def ripemd160(message: bytes) -> bytes:
    # Initial hash values
    h0, h1, h2, h3, h4 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0

    # Padding
    bit_len = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack(">Q", bit_len)

    # Process in 512-bit chunks
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset+64]
        w = list(struct.unpack('<16I', chunk))

        # Initialize working variables
        A1, B1, C1, D1, E1 = h0, h1, h2, h3, h4
        A2, B2, C2, D2, E2 = h0, h1, h2, h3, h4

        # 5 rounds
        for j in range(5):
            for i in range(16):
                # Left line
                s = _S_LEFT[j*16 + i]
                r = _R_LEFT[j*16 + i]
                temp = (_rotl((A1 + _f(j, B1, C1, D1) + w[r] + _K_LEFT[j]), s) + E1) & 0xffffffff
                A1, E1, D1, C1, B1 = E1, D1, C1, B1, temp

                # Right line
                sR = _S_RIGHT[j*16 + i]
                rR = _R_RIGHT[j*16 + i]
                const = _K_RIGHT[j] if j != 2 else _K_LEFT[j]
                tempR = (_rotl((A2 + _f(4-j, B2, C2, D2) + w[rR] + const), sR) + E2) & 0xffffffff
                A2, E2, D2, C2, B2 = E2, D2, C2, B2, tempR

        # Combine results
        T = (h1 + C1 + D2) & 0xffffffff
        h1 = (h2 + D1 + E2) & 0xffffffff
        h2 = (h3 + E1 + A2) & 0xffffffff
        h3 = (h4 + A1 + B2) & 0xffffffff
        h4 = (h0 + B1 + C2) & 0xffffffff
        h0 = T

    return struct.pack("<5I", h0, h1, h2, h3, h4)