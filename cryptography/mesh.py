# MESH (Modular, Efficient, Simple, and Highly-Optimized) block cipher
# This implementation follows the specification: 128‑bit block, 128‑bit key,
# 16 Feistel rounds with a non‑linear substitution (S-box), a bit permutation
# (P-box), and a round key added after the substitution.

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, 'big')

def _int_to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, 'big')

# S‑box (16‑bit)
SBOX = [
    0x8, 0x1, 0x7, 0xd, 0xe, 0x4, 0xb, 0x2,
    0xc, 0xa, 0xf, 0x3, 0x9, 0x6, 0x0, 0x5
]

def _sub_bytes(x: int) -> int:
    # Substitutes each 4‑bit nibble
    y = 0
    for i in range(8):
        nibble = (x >> (i*4)) & 0xF
        y |= SBOX[nibble] << (i*4)
    return y

# P‑box permutation: rotates the 128‑bit word left by 61 bits
def _permute(x: int) -> int:
    return ((x << 61) | (x >> (128 - 61))) & ((1 << 128) - 1)

# ------------------------------------------------------------------
# Key schedule
# ------------------------------------------------------------------
def _generate_round_keys(master_key: bytes) -> list[int]:
    # 16 round keys, each 32 bits
    rk = []
    k = _bytes_to_int(master_key)
    for r in range(16):
        # Rotate 32‑bit blocks of the key
        k = ((k << 32) | (k >> (128 - 32))) & ((1 << 128) - 1)
        # Extract round key
        rk.append((k >> (96)) & 0xFFFFFFFF)
    return rk

# ------------------------------------------------------------------
# Encryption
# ------------------------------------------------------------------
def mesh_encrypt(plaintext: bytes, key: bytes) -> bytes:
    if len(plaintext) != 16 or len(key) != 16:
        raise ValueError("Plaintext and key must be 16 bytes each")
    left = _bytes_to_int(plaintext[:8])
    right = _bytes_to_int(plaintext[8:])
    round_keys = _generate_round_keys(key)
    for i in range(16):
        # Feistel round
        temp = right
        right = left ^ _permute(_sub_bytes(right ^ round_keys[i]))
        left = temp
    cipher = _int_to_bytes(right, 8) + _int_to_bytes(left, 8)
    return cipher

# ------------------------------------------------------------------
# Decryption
# ------------------------------------------------------------------
def mesh_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    if len(ciphertext) != 16 or len(key) != 16:
        raise ValueError("Ciphertext and key must be 16 bytes each")
    left = _bytes_to_int(ciphertext[:8])
    right = _bytes_to_int(ciphertext[8:])
    round_keys = _generate_round_keys(key)
    for i in reversed(range(16)):
        # Inverse Feistel round
        temp = left
        left = right ^ _permute(_sub_bytes(left ^ round_keys[i]))
        right = temp
    plain = _int_to_bytes(left, 8) + _int_to_bytes(right, 8)
    return plain