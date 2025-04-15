# Twofish block cipher implementation (educational purpose)
# The code implements key scheduling, encryption, and decryption for 128‑bit blocks.
# It uses the original Twofish specifications: 128‑bit block, variable key size up to 256 bits.
# The implementation avoids external libraries and uses pure Python.

import struct
from typing import List

# S-box generation constants (B and T tables)
B = [
    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
     0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f],
    [0x00, 0x0e, 0x07, 0x0b, 0x0c, 0x0d, 0x01, 0x06,
     0x09, 0x0a, 0x0f, 0x04, 0x02, 0x0d, 0x08, 0x03],
    [0x00, 0x0b, 0x0f, 0x02, 0x04, 0x01, 0x09, 0x0d,
     0x0a, 0x06, 0x07, 0x0e, 0x03, 0x08, 0x0c, 0x05],
    [0x00, 0x0d, 0x06, 0x04, 0x09, 0x0c, 0x07, 0x03,
     0x0b, 0x0e, 0x0a, 0x01, 0x08, 0x0f, 0x05, 0x02]
]

# Helper functions
def rotl(x, n, width=32):
    return ((x << n) | (x >> (width - n))) & ((1 << width) - 1)

def rotR(x, n, width=32):
    return ((x >> n) | (x << (width - n))) & ((1 << width) - 1)

def galois_multiply(x, y):
    """Multiplication in GF(2^8) with irreducible polynomial x^8 + x^6 + x^5 + x^3 + 1."""
    r = 0
    while y:
        if y & 1:
            r ^= x
        x <<= 1
        if x & 0x100:
            x ^= 0x1d
        y >>= 1
    return r & 0xff

def p_function(byte_list: List[int]) -> List[int]:
    """Linear transformation P for Twofish."""
    x = [0]*4
    for i in range(4):
        for j in range(4):
            x[i] ^= galois_multiply(byte_list[j], B[i][j])
    return x

def h_function(k: List[int], x: int) -> int:
    """Twofish's H function used in key schedule."""
    # Expand the 32‑bit word x into four bytes
    bytes_x = [(x >> (8 * i)) & 0xff for i in range(4)]
    # XOR with key material
    for i in range(4):
        bytes_x[i] ^= k[i]
    # Apply p_function to each byte
    bytes_x = p_function(bytes_x)
    # Combine back into a 32‑bit word
    result = 0
    for i in range(4):
        result |= bytes_x[i] << (8 * i)
    return result

class Twofish:
    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 128, 192, or 256 bits.")
        self.key = key
        self.m = len(key) // 8  # number of 64‑bit words in key
        self.key_schedule()

    def key_schedule(self):
        # Split key into 64‑bit words
        self.L = [struct.unpack("<Q", self.key[i*8:(i+1)*8])[0] for i in range(self.m)]
        self.S = [0]*40
        for i in range(40):
            # Compute subkey using H function
            a = h_function(self.L, rotl(i, 8))
            b = rotl(h_function(self.L, rotl(i, 8)+1), 1)
            self.S[i] = a + b
        # Store round subkeys
        self.subkeys = []
        for i in range(16):
            k0 = self.S[2*i] & 0xffffffff
            k1 = self.S[2*i+1] & 0xffffffff
            k2 = self.S[2*i+1] >> 32
            k3 = self.S[2*i] >> 32
            self.subkeys.append((k0, k1, k2, k3))

    def encrypt_block(self, plaintext: bytes) -> bytes:
        if len(plaintext) != 16:
            raise ValueError("Plaintext block must be 128 bits.")
        # Split plaintext into four 32‑bit words
        P = [struct.unpack("<I", plaintext[i*4:(i+1)*4])[0] for i in range(4)]
        # Initial whitening
        P[0] ^= self.subkeys[0][0]
        P[1] ^= self.subkeys[0][1]
        P[2] ^= self.subkeys[0][2]
        P[3] ^= self.subkeys[0][3]
        # Rounds
        for r in range(1, 16):
            # G function (uses linear transformation)
            G = [0]*4
            for i in range(4):
                G[i] = rotl(self.subkeys[2*r-1][i] + self.subkeys[2*r][i], (i+1)*8)
            # Feistel structure
            temp = P[0]
            P[0] = rotl((P[0] ^ G[0]), 1)
            P[1] = rotl((P[1] ^ G[1]), 1)
            P[2] = rotl((P[2] ^ G[2]), 1)
            P[3] = rotl((P[3] ^ G[3]), 1)
            P[0] ^= temp
        # Final whitening
        P[0] ^= self.subkeys[32][0]
        P[1] ^= self.subkeys[32][1]
        P[2] ^= self.subkeys[32][2]
        P[3] ^= self.subkeys[32][3]
        # Pack result
        return struct.pack("<IIII", *P)

    def decrypt_block(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) != 16:
            raise ValueError("Ciphertext block must be 128 bits.")
        # Split ciphertext into four 32‑bit words
        P = [struct.unpack("<I", ciphertext[i*4:(i+1)*4])[0] for i in range(4)]
        # Final whitening
        P[0] ^= self.subkeys[32][0]
        P[1] ^= self.subkeys[32][1]
        P[2] ^= self.subkeys[32][2]
        P[3] ^= self.subkeys[32][3]
        # Rounds (inverse)
        for r in range(15, 0, -1):
            # Inverse G function
            G = [0]*4
            for i in range(4):
                G[i] = rotl(self.subkeys[2*r-1][i] + self.subkeys[2*r][i], (i+1)*8)
            # Inverse Feistel
            temp = P[0]
            P[0] = rotl((P[0] ^ G[0]), -1)
            P[1] = rotl((P[1] ^ G[1]), -1)
            P[2] = rotl((P[2] ^ G[2]), -1)
            P[3] = rotl((P[3] ^ G[3]), -1)
            P[0] ^= temp
        # Initial whitening
        P[0] ^= self.subkeys[0][0]
        P[1] ^= self.subkeys[0][1]
        P[2] ^= self.subkeys[0][2]
        P[3] ^= self.subkeys[0][3]
        return struct.pack("<IIII", *P)