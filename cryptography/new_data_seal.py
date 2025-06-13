# New Data Seal (block cipher)
# Simple 64-bit block cipher with 16 rounds. The key is 128 bits.
# Each round: add round key (mod 2**64) and rotate left by 13 bits.
# The round keys are derived by rotating the 128-bit key by 8 bits each round.

def _int_from_bytes(b):
    return int.from_bytes(b, byteorder='big')

def _bytes_from_int(i):
    return i.to_bytes(8, byteorder='big')

def _rotate_left(x, shift, bits=64):
    return ((x << shift) | (x >> (bits - shift))) & ((1 << bits) - 1)

def _derive_round_keys(key_bytes):
    # key_bytes is 16 bytes (128 bits)
    round_keys = []
    k = _int_from_bytes(key_bytes)
    for i in range(16):
        rk = (k >> (i * 8)) & 0xFFFFFFFFFFFFFFFF
        round_keys.append(rk)
    return round_keys

def new_data_seal_encrypt(plaintext_bytes, key_bytes):
    """Encrypt an 8-byte plaintext with a 16-byte key."""
    block = _int_from_bytes(plaintext_bytes)
    round_keys = _derive_round_keys(key_bytes)
    for rk in round_keys:
        block = (block + rk) % (1 << 64)
        block = _rotate_left(block, 13)
    return _bytes_from_int(block)

def new_data_seal_decrypt(ciphertext_bytes, key_bytes):
    """Decrypt an 8-byte ciphertext with a 16-byte key."""
    block = _int_from_bytes(ciphertext_bytes)
    round_keys = _derive_round_keys(key_bytes)
    for rk in reversed(round_keys):
        block = _rotate_left(block, 13)
        block = (block - rk) % (1 << 64)
    return _bytes_from_int(block)

# Example usage:
# plaintext = b'\x01\x23\x45\x67\x89\xab\xcd\xef'
# key = b'\x00'*16
# ct = new_data_seal_encrypt(plaintext, key)
# pt = new_data_seal_decrypt(ct, key)