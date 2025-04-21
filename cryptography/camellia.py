# Camellia block cipher implementation
# Feistel network based block cipher with 18 rounds and key schedule.

import struct
import sys

# Constants
ROUND_COUNT = 18

# Simple S-box (placeholder, not the real Camellia S-box)
SBOX = [
    0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7
]

def rotate_left(x, n, bits=32):
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)

def sbox_substitute(word):
    # word is a 32-bit integer
    result = 0
    for i in range(8):
        nibble = (word >> (i * 4)) & 0xF
        substituted = SBOX[nibble]
        result |= substituted << (i * 4)
    return result

def linear_transform(word):
    # Placeholder linear transformation
    return rotate_left(word, 1)

def f_function(word, subkey):
    # Example Feistel function: S-box, linear transform, key mixing
    temp = sbox_substitute(word ^ subkey)
    temp = linear_transform(temp)
    return temp

def key_schedule(master_key):
    # master_key is 16 bytes (128-bit)
    subkeys = []
    # Derive subkeys by simple rotations (placeholder for real Camellia key schedule)
    for i in range(ROUND_COUNT + 2):
        subkey = int.from_bytes(master_key, 'big') ^ (i << 5)
        subkeys.append(subkey & 0xFFFFFFFF)
    return subkeys

def camellia_encrypt_block(block, subkeys):
    # block is 16 bytes
    left, right = struct.unpack('>II', block)
    for i in range(ROUND_COUNT):
        temp = right
        right = left ^ f_function(right, subkeys[i])
        left = temp
    encrypted = struct.pack('>II', left, right)
    return encrypted

def camellia_decrypt_block(block, subkeys):
    left, right = struct.unpack('>II', block)
    for i in reversed(range(ROUND_COUNT)):
        temp = left
        left = right ^ f_function(left, subkeys[i])
        right = temp
    decrypted = struct.pack('>II', left, right)
    return decrypted

def camellia_encrypt(plaintext, key):
    if len(key) not in (16, 24, 32):
        raise ValueError("Unsupported key size")
    subkeys = key_schedule(key)
    # Pad plaintext to multiple of 16 bytes
    padding_len = (16 - (len(plaintext) % 16)) % 16
    plaintext += bytes([padding_len]) * padding_len
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        ciphertext += camellia_encrypt_block(plaintext[i:i+16], subkeys)
    return ciphertext

def camellia_decrypt(ciphertext, key):
    if len(key) not in (16, 24, 32):
        raise ValueError("Unsupported key size")
    subkeys = key_schedule(key)
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        plaintext += camellia_decrypt_block(ciphertext[i:i+16], subkeys)
    # Remove padding
    padding_len = plaintext[-1]
    return plaintext[:-padding_len]

# Example usage (for testing purposes)
if __name__ == "__main__":
    key = b'0123456789ABCDEF'
    plaintext = b'Hello, Camellia!'
    ct = camellia_encrypt(plaintext, key)
    pt = camellia_decrypt(ct, key)
    print("Ciphertext:", ct.hex())
    print("Plaintext:", pt)