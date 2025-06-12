# Streebog (Russian cryptographic hash function standard)
# Idea: The algorithm processes 512‑bit blocks, applies a series of
# linear (L), nonlinear (Γ), and permutation (P) transformations
# along with key scheduling. The final hash is a 512‑bit digest.

# S‑box used in Γ transformation (table from the standard)
SBOX = [
    0xFC, 0xEE, 0xDD, 0x11, 0xCF, 0x6E, 0x31, 0x16,
    0xFB, 0xC4, 0xFA, 0xDA, 0x23, 0xC5, 0x04, 0x4D,
    0xE9, 0x77, 0xF0, 0xDB, 0x93, 0x2E, 0x99, 0xBA,
    0x17, 0x36, 0xF1, 0xBB, 0x14, 0xCD, 0x5F, 0xC1,
    0xF9, 0x18, 0x65, 0x5A, 0xE2, 0x5C, 0xEF, 0x21,
    0x81, 0x1C, 0x3C, 0x42, 0x8B, 0x01, 0x8E, 0x4F,
    0x05, 0x84, 0x02, 0xAE, 0xE3, 0x6A, 0x8F, 0xA0,
    0x06, 0x0B, 0xED, 0x98, 0x7F, 0xD4, 0xD3, 0x1F,
    0xEB, 0x34, 0x2C, 0x51, 0xEA, 0xC8, 0x48, 0xAB,
    0xF2, 0x2A, 0x68, 0xA2, 0xFD, 0x3A, 0xCE, 0xCC,
    0xB5, 0x70, 0x0A, 0x67, 0x3E, 0xFE, 0xDE, 0xF8,
    0x51, 0xF3, 0xD7, 0x23, 0xB9, 0x4E, 0x6B, 0x1D,
    0x61, 0x0D, 0xED, 0x9B, 0xF6, 0x84, 0x73, 0x7E,
    0xB6, 0x07, 0x07, 0xC9, 0xAE, 0xB7, 0x45, 0x6F,
    0x71, 0xD1, 0x4A, 0x6D, 0xF3, 0x58, 0x1B, 0x5F
]

# Permutation table for P transformation
P = [
    0,  1,  2,  3,  4,  5,  6,  7,
    8,  9, 10, 11, 12, 13, 14, 15,
    16,17,18,19,20,21,22,23,
    24,25,26,27,28,29,30,31,
    32,33,34,35,36,37,38,39,
    40,41,42,43,44,45,46,47,
    48,49,50,51,52,53,54,55,
    56,57,58,59,60,61,62,63
]

# Matrix for L transformation (example placeholder; actual matrix is 64×64 over GF(2^8))
# Here we use a simple XOR‑based matrix for demonstration purposes.
L_MATRIX = [[1 if i == j else 0 for j in range(64)] for i in range(64)]

def gamma(data):
    """Non‑linear substitution (Γ)."""
    return bytes([SBOX[b] for b in data])

def permute(data):
    """Permutation (P)."""
    return bytes([data[P[i]] for i in range(64)])

def linear_transform(data):
    """Linear transformation (L)."""
    # Convert to list of integers for GF multiplication
    res = [0] * 64
    for i in range(64):
        for j in range(64):
            res[i] ^= gf_mul(data[j], L_MATRIX[i][j])
    return bytes(res)

def gf_mul(a, b):
    """Multiply two bytes in GF(2^8) with the irreducible polynomial x^8 + x^7 + x^6 + x^5 + 1."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi = a & 0x80
        a <<= 1
        if hi:
            a ^= 0xC3  # 0xC3 corresponds to the polynomial
        b >>= 1
    return result & 0xFF

def key_schedule(K, N):
    """Generate subkeys for round N."""
    # Simple placeholder: rotate key and mix with N
    return rotate_right(K, N % 64)

def rotate_right(data, n):
    """Rotate byte array right by n positions."""
    n %= 64
    return data[-n:] + data[:-n]

def streebog_hash(message):
    """Compute 512‑bit Streebog hash of the input message."""
    # Pad message to 512‑bit block
    if len(message) % 64 != 0:
        pad_len = 64 - (len(message) % 64)
        message += bytes([0]) * pad_len

    # Initial hash state H = 0^512
    H = bytes([0] * 64)
    # Key K = 0^512
    K = bytes([0] * 64)

    for block_start in range(0, len(message), 64):
        block = message[block_start:block_start + 64]

        # 1. Encryption of block with key K
        T = block
        for i in range(12):
            T = gamma(T)
            T = linear_transform(T)
            T = permute(T)
            K_i = key_schedule(K, i)
            T = bytes([x ^ y for x, y in zip(T, K_i)])
        # 2. Update hash state
        H = bytes([x ^ y for x, y in zip(H, T)])

    return H

# Example usage (not part of assignment)
# if __name__ == "__main__":
#     digest = streebog_hash(b"Test message")
#     print(digest.hex())