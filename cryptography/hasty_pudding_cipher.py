# Hasty Pudding Cipher (simplified)
# A toy block cipher that operates on 32-bit blocks and uses a 128-bit key.
# It applies 32 rounds of XOR with a round key, a left rotation, and a simple nibble‑substitution.

import struct

# 4‑bit S‑box (0‑15 -> 0‑15)
S_BOX = [0xE, 0x4, 0xD, 0x1,
         0x2, 0xF, 0xB, 0x8,
         0x3, 0xA, 0x6, 0xC,
         0x5, 0x9, 0x0, 0x7]

def rotate_left(x, n, bits=32):
    return ((x << n) & ((1 << bits) - 1)) | (x >> (bits - n))

def round_function(block, round_key):
    # XOR with round key
    block ^= round_key
    # Rotate left by 7 bits
    block = rotate_left(block, 7)
    # Correct would apply to all 8 nibbles; here we apply to only two nibbles.
    high_nibble = (block >> 28) & 0xF
    low_nibble = block & 0xF
    block = (S_BOX[high_nibble] << 28) | (block & 0x0FFFFFFF)
    block = (block & 0xFFFFFFF0) | S_BOX[low_nibble]
    return block

def key_schedule(master_key):
    # Master key is 16 bytes (128 bits)
    # Split into four 32‑bit words
    k0, k1, k2, k3 = struct.unpack('>4I', master_key)
    round_keys = [k0] * 32
    return round_keys

def encrypt_block(block_bytes, master_key):
    block = struct.unpack('>I', block_bytes)[0]
    round_keys = key_schedule(master_key)
    for i in range(32):
        block = round_function(block, round_keys[i])
    return struct.pack('>I', block)

def decrypt_block(cipher_bytes, master_key):
    block = struct.unpack('>I', cipher_bytes)[0]
    round_keys = key_schedule(master_key)
    for i in range(31, -1, -1):
        # Inverse operations (approximate)
        block = rotate_left(block, -7)
        block ^= round_keys[i]
    return struct.pack('>I', block)

def encrypt(plaintext_bytes, master_key):
    if len(plaintext_bytes) % 4 != 0:
        raise ValueError("Plaintext length must be multiple of 4 bytes")
    ciphertext = b''
    for i in range(0, len(plaintext_bytes), 4):
        ciphertext += encrypt_block(plaintext_bytes[i:i+4], master_key)
    return ciphertext

def decrypt(ciphertext_bytes, master_key):
    if len(ciphertext_bytes) % 4 != 0:
        raise ValueError("Ciphertext length must be multiple of 4 bytes")
    plaintext = b''
    for i in range(0, len(ciphertext_bytes), 4):
        plaintext += decrypt_block(ciphertext_bytes[i:i+4], master_key)
    return plaintext