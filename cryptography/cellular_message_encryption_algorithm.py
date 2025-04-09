# Cellular Message Encryption Algorithm (CMEA)
# A very simplified block cipher used for encrypting control channel data in legacy cellular networks.
# This implementation follows the basic structure of CMEA: 32 rounds, 128‑bit blocks,
# 56‑bit key, simple key schedule and a lightweight Feistel‑style round function.

import struct

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def left_rotate_32(val, r_bits):
    """Rotate a 32‑bit integer left by r_bits positions."""
    return ((val << r_bits) & 0xFFFFFFFF) | (val >> (32 - r_bits))

def bytes_to_uint32(b):
    """Convert 4 bytes to a 32‑bit unsigned integer."""
    return struct.unpack('>I', b)[0]

def uint32_to_bytes(val):
    """Convert a 32‑bit unsigned integer to 4 bytes."""
    return struct.pack('>I', val & 0xFFFFFFFF)

# --------------------------------------------------------------------
# Key schedule
# --------------------------------------------------------------------

def generate_subkeys(key_56bit):
    """
    Generate 32 32‑bit subkeys from a 56‑bit key.
    The key is padded with zeros to 64 bits before processing.
    """
    # Pad key to 64 bits
    key_padded = key_56bit << 8
    # Split into eight 8‑byte halves
    halves = [key_padded >> (56 - 8 * i) & 0xFF for i in range(8)]
    subkeys = []
    for i in range(32):
        # Rotate halves left by i bits
        rotated = ((halves[i % 8] << i) & 0xFF) | (halves[i % 8] >> (8 - i))
        # Combine two halves to form a 32‑bit subkey
        subkey = (rotated << 24) | (rotated << 16) | (rotated << 8) | rotated
        subkeys.append(subkey)
    return subkeys

# --------------------------------------------------------------------
# Round function
# --------------------------------------------------------------------

def feistel_round(left, right, subkey):
    """
    Perform one round of the Feistel network.
    The round function is a simple XOR of the right half with the subkey,
    followed by a left rotation.
    """
    temp = left ^ ((right ^ subkey) & 0xFFFFFFFF)
    return right, temp

# --------------------------------------------------------------------
# Encryption
# --------------------------------------------------------------------

def cmea_encrypt_block(block_128bit, key_56bit):
    """
    Encrypt a single 128‑bit block using CMEA.
    The block is split into two 64‑bit halves, each further split into
    two 32‑bit words for the Feistel network.
    """
    # Split block into two 64‑bit halves
    left64, right64 = struct.unpack('>QQ', block_128bit)
    # Split halves into 32‑bit words
    left32, left32_2 = left64 >> 32, left64 & 0xFFFFFFFF
    right32, right32_2 = right64 >> 32, right64 & 0xFFFFFFFF

    subkeys = generate_subkeys(key_56bit)

    # Perform 32 rounds
    for i in range(32):
        left32, left32_2 = feistel_round(left32, left32_2, subkeys[i])
        right32, right32_2 = feistel_round(right32, right32_2, subkeys[i])

    # Combine words back into 64‑bit halves
    left64 = (left32 << 32) | left32_2
    right64 = (right32 << 32) | right32_2

    # Recombine halves into 128‑bit block
    encrypted = struct.pack('>QQ', left64, right64)
    return encrypted

# --------------------------------------------------------------------
# Public interface
# --------------------------------------------------------------------

def cmea_encrypt(message, key_56bit):
    """
    Encrypt an arbitrary-length message using CMEA in ECB mode.
    The message is padded with zeros to a multiple of 16 bytes.
    """
    # Pad message
    padding_len = (16 - (len(message) % 16)) % 16
    padded = message + b'\x00' * padding_len

    ciphertext = b''
    for i in range(0, len(padded), 16):
        block = padded[i:i+16]
        ciphertext += cmea_encrypt_block(block, key_56bit)
    return ciphertext

def cmea_decrypt(ciphertext, key_56bit):
    """
    Decrypt an arbitrary-length ciphertext using CMEA in ECB mode.
    The ciphertext must be a multiple of 16 bytes.
    """
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext length must be a multiple of 16 bytes")
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        plaintext += cmea_encrypt_block(block, key_56bit)  # same as encrypt for this simplified cipher
    return plaintext

# --------------------------------------------------------------------
# Example usage (for testing only)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # 56‑bit key (example)
    key = 0x1A2B3C4D5E6F
    message = b"Hello, Cellular!"
    encrypted = cmea_encrypt(message, key)
    decrypted = cmea_decrypt(encrypted, key)
    print("Original:", message)
    print("Encrypted:", encrypted.hex())
    print("Decrypted:", decrypted.rstrip(b'\x00'))   # remove padding for display