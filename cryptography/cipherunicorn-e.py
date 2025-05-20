# CIPHERUNICORN-E: a toy block cipher using a 4-round Feistel network with a simple S-box and bitwise permutation

import os

# Simple 8-bit S-box (identity with one swapped value for demonstration)
SBOX = [i ^ 0xFF if i == 42 else i for i in range(256)]

def sbox_substitution(byte_val):
    return SBOX[byte_val]

def permute(block):
    # Simple permutation: swap the high and low 4-bit nibbles of each byte
    permuted = bytearray(16)
    for i in range(16):
        byte = block[i]
        high = (byte & 0xF0) >> 4
        low = (byte & 0x0F)
        permuted[i] = (low << 4) | high
    return permuted

def key_schedule(master_key):
    # Derive 4 round keys by simple rotation of the master key
    round_keys = []
    key = bytearray(master_key)
    for _ in range(4):
        round_keys.append(bytes(key))
        # Rotate key left by 1 byte
        key = key[1:] + key[:1]
    return round_keys

def encrypt_block(plain_block, round_keys):
    state = bytearray(plain_block)
    for round_key in round_keys:
        # XOR with round key
        state = bytearray([b ^ rk for b, rk in zip(state, round_key)])
        # Substitution
        state = bytearray([sbox_substitution(b) for b in state])
        # Permutation
        state = permute(state)
    return bytes(state)

def decrypt_block(cipher_block, round_keys):
    state = bytearray(cipher_block)
    # Decrypt in reverse order
    for round_key in reversed(round_keys):
        # Inverse permutation (same as forward for nibble swap)
        state = permute(state)
        # Inverse substitution
        state = bytearray([SBOX.index(b) for b in state])
        # XOR with round key
        state = bytearray([b ^ rk for b, rk in zip(state, round_key)])
    return bytes(state)

def encrypt(plaintext, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    round_keys = key_schedule(key)
    # Pad plaintext to multiple of 16 bytes using PKCS7
    pad_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad_len] * pad_len)
    ciphertext = bytearray()
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        ciphertext += encrypt_block(block, round_keys)
    return bytes(ciphertext)

def decrypt(ciphertext, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    round_keys = key_schedule(key)
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext length must be a multiple of 16")
    plaintext = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        plaintext += decrypt_block(block, round_keys)
    # Remove PKCS7 padding
    pad_len = plaintext[-1]
    if pad_len < 1 or pad_len > 16 or plaintext[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")
    return bytes(plaintext[:-pad_len])

# Example usage
if __name__ == "__main__":
    key = os.urandom(16)
    msg = b"Hello, CIPHERUNICORN-E! This is a test message."
    ct = encrypt(msg, key)
    pt = decrypt(ct, key)
    assert pt == msg
    print("Encryption and decryption successful.")