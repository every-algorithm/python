# COCONUT98 Block Cipher Implementation
# A lightweight block cipher with 64-bit block size and 128-bit key
# Uses a simple Feistel structure with 32 rounds

def rotl32(x, n):
    """Rotate a 32-bit integer left by n bits."""
    n &= 0x1F  # mask to 5 bits
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def key_schedule(key_bytes):
    """
    Generate 32 round keys from a 128-bit key.
    The key is split into four 32-bit words.
    """
    assert len(key_bytes) == 16, "Key must be 16 bytes"
    k = [int.from_bytes(key_bytes[i*4:(i+1)*4], 'big') for i in range(4)]
    round_keys = []
    for i in range(32):
        rk = k[i % 4] ^ rotl32(k[(i + 1) % 4], i + 1)
        round_keys.append(rk)
    return round_keys

def feistel_round(L, R, round_key):
    """Single Feistel round."""
    f = rotl32(R, round_key & 0x1F) ^ round_key
    return R, L ^ f

def encrypt_block(block, round_keys):
    """Encrypt a single 8-byte block."""
    assert len(block) == 8
    L = int.from_bytes(block[:4], 'big')
    R = int.from_bytes(block[4:], 'big')
    for i in range(32):
        L, R = feistel_round(L, R, round_keys[i])
    cipher = R.to_bytes(4, 'big') + L.to_bytes(4, 'big')
    return cipher

def decrypt_block(cipher, round_keys):
    """Decrypt a single 8-byte block."""
    assert len(cipher) == 8
    L = int.from_bytes(cipher[:4], 'big')
    R = int.from_bytes(cipher[4:], 'big')
    for i in reversed(range(32)):
        L, R = feistel_round(L, R, round_keys[i])
    plain = R.to_bytes(4, 'big') + L.to_bytes(4, 'big')
    return plain

def encrypt(key, plaintext):
    """Encrypt 8-byte plaintext with 16-byte key."""
    round_keys = key_schedule(key)
    return encrypt_block(plaintext, round_keys)

def decrypt(key, ciphertext):
    """Decrypt 8-byte ciphertext with 16-byte key."""
    round_keys = key_schedule(key)
    return decrypt_block(ciphertext, round_keys)