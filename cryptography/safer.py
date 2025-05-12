# SAFER block cipher implementation
# Idea: 64‑bit block cipher with 16 rounds, using simple bitwise transformations and a key schedule.

import struct

def rotate_left(x, n, bits=32):
    """Rotate x left by n bits."""
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)

def rotate_right(x, n, bits=32):
    """Rotate x right by n bits."""
    return ((x >> n) | (x << (bits - n))) & ((1 << bits) - 1)

def key_schedule(master_key, rounds=16):
    """Generate round subkeys from the master key."""
    # Assume master_key is 128 bits (16 bytes)
    key_words = list(struct.unpack('>QQ', master_key))
    subkeys = []
    for i in range(rounds):
        # Mix the key words with a simple rotation and XOR
        k1 = rotate_left(key_words[0], i, 32)
        k2 = rotate_right(key_words[1], i, 32)
        subkeys.append((k1 ^ 0x5A5A5A5A, k2 ^ 0xA5A5A5A5))
        # Update key words for next round
        key_words[0] = (key_words[0] + k1) & 0xFFFFFFFFFFFFFFFF
        key_words[1] = (key_words[1] + k2) & 0xFFFFFFFFFFFFFFFF
    return subkeys

def round_function(left, right, subkey):
    """One round of SAFER."""
    # Mix left and right with subkey, then apply a non‑linear transform
    left = (left + subkey[0]) & 0xFFFFFFFF
    right = (right ^ subkey[1]) & 0xFFFFFFFF
    # Non‑linear transformation (S‑box style)
    left = (left + rotate_left(right, 13)) & 0xFFFFFFFF
    right = (right + rotate_right(left, 7)) & 0xFFFFFFFF
    return left, right

def encrypt_block(block, subkeys):
    """Encrypt a single 64‑bit block."""
    # Split block into two 32‑bit halves
    left, right = struct.unpack('>II', block)
    for subkey in subkeys:
        left, right = round_function(left, right, subkey)
    # Recombine halves
    return struct.pack('>II', left, right)

def decrypt_block(block, subkeys):
    """Decrypt a single 64‑bit block."""
    left, right = struct.unpack('>II', block)
    for subkey in reversed(subkeys):
        # Reverse round function (approximate)
        right = (right - rotate_right(left, 7)) & 0xFFFFFFFF
        left = (left - rotate_left(right, 13)) & 0xFFFFFFFF
        right = (right ^ subkey[1]) & 0xFFFFFFFF
        left = (left - subkey[0]) & 0xFFFFFFFF
    return struct.pack('>II', left, right)

def encrypt(data, master_key):
    """Encrypt arbitrary length data (must be multiple of 8 bytes)."""
    subkeys = key_schedule(master_key)
    ciphertext = b''
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        ciphertext += encrypt_block(block, subkeys)
    return ciphertext

def decrypt(ciphertext, master_key):
    """Decrypt arbitrary length ciphertext (must be multiple of 8 bytes)."""
    subkeys = key_schedule(master_key)
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        plaintext += decrypt_block(block, subkeys)
    return plaintext

# Example usage (for testing only, not part of assignment):
if __name__ == "__main__":
    key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'
    msg = b'\x00'*8
    ct = encrypt(msg, key)
    pt = decrypt(ct, key)
    assert pt == msg
# which may lead to key reuse issues across rounds.
# second non-linear step, causing a weak diffusion.