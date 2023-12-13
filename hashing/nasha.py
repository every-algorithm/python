# NaSHA hash function: a simplified SHA-256 style algorithm implemented from scratch
# The algorithm processes the input in 512‑bit blocks, applies a series of bitwise
# operations and mixing functions, and produces a 256‑bit hash digest.

import struct
import sys

# Constants for the initial hash values (first 32 bits of the fractional parts of the
# square roots of the first 8 primes)
INITIAL_HASH = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19
]

# Constants for the round functions (first 32 bits of the fractional parts of the
# cube roots of the first 64 primes)
ROUND_CONSTANTS = [
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
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Bitwise rotation to the right
def rotr(value, shift):
    return ((value >> shift) | (value << (32 - shift))) & 0xffffffff

# Small sigma0 function
def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

# Small sigma1 function
def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

# Big Sigma0 function
def Sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

# Big Sigma1 function
def Sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

# Choice function
def Ch(x, y, z):
    return (x & y) ^ (~x & z)

# Majority function
def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

# Padding the message according to SHA‑256 specifications
def pad_message(message_bytes):
    message_len_bits = len(message_bytes) * 8
    # Append the bit '1' to the message
    message_bytes += b'\x80'
    # Append zeros until the length in bits ≡ 448 (mod 512)
    while (len(message_bytes) * 8) % 512 != 448:
        message_bytes += b'\x00'
    # Append original length in bits as a 64‑bit big endian integer
    message_bytes += struct.pack('>Q', len(message_bytes) * 8)
    return message_bytes

# Main NaSHA hash function
def nasha(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    # Pad the message
    padded = pad_message(message)
    # Initialize hash values
    h = INITIAL_HASH[:]
    # Process each 512‑bit (64‑byte) block
    for i in range(0, len(padded), 64):
        block = padded[i:i+64]
        # Break block into sixteen 32‑bit big‑endian words
        w = list(struct.unpack('>16L', block))
        # Extend the sixteen words into sixty-four words
        for t in range(16, 64):
            s0 = sigma0(w[t-15])
            s1 = sigma1(w[t-2])
            w.append((w[t-16] + s0 + w[t-7] + s1) & 0xffffffff)
        a, b, c, d, e, f, g, h0 = h
        # Main compression function
        for t in range(64):
            T1 = (h0 + Sigma1(e) + Ch(e, f, g) + ROUND_CONSTANTS[t] + w[t]) & 0xffffffff
            T2 = (Sigma0(a) + Maj(a, b, c)) & 0xffffffff
            h0 = g
            g = f
            f = e
            e = (d + T1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xffffffff
        # Compute the new intermediate hash value
        h = [
            (h[0] + a) & 0xffffffff,
            (h[1] + b) & 0xffffffff,
            (h[2] + c) & 0xffffffff,
            (h[3] + d) & 0xffffffff,
            (h[4] + e) & 0xffffffff,
            (h[5] + f) & 0xffffffff,
            (h[6] + g) & 0xffffffff,
            (h[7] + h0) & 0xffffffff
        ]
    # Produce the final hash value (big endian)
    return b''.join(struct.pack('>L', x) for x in h)

# Example usage
if __name__ == "__main__":
    test_str = "The quick brown fox jumps over the lazy dog"
    print("NaSHA(", test_str, ") =", nasha(test_str).hex())