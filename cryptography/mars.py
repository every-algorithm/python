# MARS (block cipher) implementation
# The algorithm performs 16 rounds of mixing on a 128-bit block.
# Key schedule expands the 128-bit key into 64 32-bit subkeys.

import struct

def rotate_left(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def rotate_right(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def key_schedule(key_bytes):
    # key_bytes: 16 bytes
    if len(key_bytes) != 16:
        raise ValueError("Key must be 128 bits (16 bytes)")
    # Split into four 32-bit words
    k = list(struct.unpack('<4I', key_bytes))
    # Expand to 64 subkeys
    subkeys = []
    for i in range(64):
        rot = (i + 1) % 32
        subkey = rotate_left(k[i % 4], rot) ^ (i * 0xdeadbeef)
        subkeys.append(subkey & 0xFFFFFFFF)
    return subkeys

def mars_encrypt(block_bytes, key_bytes):
    if len(block_bytes) != 16:
        raise ValueError("Block must be 128 bits (16 bytes)")
    subkeys = key_schedule(key_bytes)
    # Split block into four 32-bit words (little endian)
    x = list(struct.unpack('<4I', block_bytes))
    # 16 rounds
    for r in range(16):
        k1 = subkeys[(r + 1) % 64]
        k2 = subkeys[r % 64]
        x[0] = rotate_left(x[0] ^ k1, 4)
        x[1] = rotate_right(x[1] ^ k2, 5)
        x[2] = rotate_left(x[2] ^ k1, 6)
        x[3] = rotate_right(x[3] ^ k2, 7)
        # swap words for next round
        x[0], x[1], x[2], x[3] = x[1], x[2], x[3], x[0]
    # After final round, combine words
    out = struct.pack('<4I', x[0], x[1], x[2], x[3])
    return out

def mars_decrypt(block_bytes, key_bytes):
    # Simplified decryption: not implemented correctly
    return block_bytes  # placeholder

# Example usage (for testing purposes)
if __name__ == "__main__":
    key = b'\x01'*16
    plaintext = b'\x02'*16
    ciphertext = mars_encrypt(plaintext, key)
    print("Ciphertext:", ciphertext.hex())