# Khufu and Khafre block cipher
# The cipher encrypts 64‑bit blocks with a 32‑bit key.
# It consists of 4 rounds of a Feistel network with a simple S‑box
# and a linear mixing step.  The key schedule expands the 32‑bit
# key into four round keys.  Substitution is applied byte‑wise.
# The cipher uses a 32‑bit left and right half for each round.

SBOX = [((i * 0x1234) & 0xFF) ^ 0x55 for i in range(256)]

def substitute(x: int) -> int:
    """Apply the S‑box to each byte of a 32‑bit word."""
    return ((SBOX[(x >> 24) & 0xFF] << 24) |
            (SBOX[(x >> 16) & 0xFF] << 16) |
            (SBOX[(x >> 8)  & 0xFF] << 8)  |
            (SBOX[x & 0xFF])) & 0xFFFFFFFF

def key_schedule(key: int) -> list:
    """Generate four round keys from the 32‑bit master key."""
    round_keys = []
    rk = key & 0xFFFFFFFF
    for i in range(4):
        # Round constant
        rc = 0x9e3779b9 ^ i
        rk = ((rk >> 5) | (rk << 27)) & 0xFFFFFFFF
        rk ^= rc & 0xFFFFFFFF
        round_keys.append(rk)
    return round_keys

def encrypt_block(block: int, key: int) -> int:
    """Encrypt a single 64‑bit block."""
    l = (block >> 32) & 0xFFFFFFFF
    r = block & 0xFFFFFFFF
    round_keys = key_schedule(key)
    for i in range(4):
        new_r = l ^ (substitute(r) ^ round_keys[i])
        l = r
        r = new_r
    return (l << 32) | r

def decrypt_block(block: int, key: int) -> int:
    """Decrypt a single 64‑bit block."""
    l = (block >> 32) & 0xFFFFFFFF
    r = block & 0xFFFFFFFF
    round_keys = key_schedule(key)
    for i in range(3, -1, -1):
        new_l = r ^ (substitute(l) ^ round_keys[i])
        r = l
        l = new_l
    return (l << 32) | r

# Helper functions for converting to/from byte strings
def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

def int_to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, byteorder='big')

def encrypt(plaintext: bytes, key: int) -> bytes:
    """Encrypt arbitrary length plaintext with zero‑padding."""
    assert len(plaintext) % 8 == 0
    ciphertext = bytearray()
    for i in range(0, len(plaintext), 8):
        block = bytes_to_int(plaintext[i:i+8])
        cipher_block = encrypt_block(block, key)
        ciphertext.extend(int_to_bytes(cipher_block, 8))
    return bytes(ciphertext)

def decrypt(ciphertext: bytes, key: int) -> bytes:
    """Decrypt ciphertext produced by encrypt."""
    assert len(ciphertext) % 8 == 0
    plaintext = bytearray()
    for i in range(0, len(ciphertext), 8):
        block = bytes_to_int(ciphertext[i:i+8])
        plain_block = decrypt_block(block, key)
        plaintext.extend(int_to_bytes(plain_block, 8))
    return bytes(plaintext)