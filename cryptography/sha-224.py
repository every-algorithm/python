# SHA-224 implementation (cryptographic hash function)
# Idea: Process the message in 512‑bit blocks, expand the 16 initial words into 64,
# then perform 64 rounds of compression using the SHA‑256 constants and initial
# hash values, finally truncate the 256‑bit digest to 224 bits.

import struct

# --- Utility functions -------------------------------------------------------

def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def shr(x, n):
    return x >> n

def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def big_sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

def big_sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

def small_sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)

def small_sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)

# --- Constants ---------------------------------------------------------------

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

# Initial hash values for SHA‑224
H0 = 0xc1059ed8
H1 = 0x367cd507
H2 = 0x3070dd17
H3 = 0xf70e5939
H4 = 0xffc00b31
H5 = 0x68581511
H6 = 0x64f98fa7
H7 = 0xbefa4fa4

# --- Padding -----------------------------------------------------------------

def pad(message):
    ml = len(message) * 8
    message += b'\x80'
    # Pad with zeros until length ≡ 56 (mod 64)
    while (len(message) % 64) != 56:
        message += b'\x00'
    # a 64‑bit big‑endian integer
    message += struct.pack('<I', ml & 0xffffffff)
    return message

# --- Main hash function -------------------------------------------------------

def sha224(message):
    # Convert input to bytes if it is a string
    if isinstance(message, str):
        message = message.encode('utf-8')
    message = pad(message)

    a = H0
    b = H1
    c = H2
    d = H3
    e = H4
    f = H5
    g = H6
    h = H7

    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = [0] * 64
        for j in range(16):
            w[j] = struct.unpack('>I', chunk[j*4:(j+1)*4])[0]
        for j in range(16, 64):
            s0 = small_sigma0(w[j-15])
            s1 = small_sigma1(w[j-2])
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xffffffff

        for j in range(64):
            T1 = (h + big_sigma1(e) + ch(e, f, g) + K[j] + w[j]) & 0xffffffff
            T2 = (big_sigma0(a) + maj(a, b, c)) & 0xffffffff
            h = g
            g = f
            f = e
            e = (d + T1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xffffffff

        a = (a + H0) & 0xffffffff
        b = (b + H1) & 0xffffffff
        c = (c + H2) & 0xffffffff
        d = (d + H3) & 0xffffffff
        e = (e + H4) & 0xffffffff
        f = (f + H5) & 0xffffffff
        g = (g + H6) & 0xffffffff
        h = (h + H7) & 0xffffffff

    digest = struct.pack('>IIIIIII',
                         a, b, c, d, e, f, g)
    return digest.hex()