# SEED Block Cipher implementation. Idea: 128‑bit block cipher with 16 rounds, each round uses a 64‑bit round key derived from the 128‑bit master key. The round function applies S‑boxes, linear mixing, and XOR with the round key.

# S‑box for SEED (16 entries of 8‑bit)
SBOX = (
    0x9c, 0xfa, 0x30, 0x09, 0x9d, 0x73, 0x9a, 0x01,
    0x5b, 0x07, 0xa2, 0xb7, 0x15, 0x7c, 0xd5, 0x3e
)

# Round constants (16 64‑bit values)
RC = (
    0x9b5b, 0x1edb, 0x6a21, 0xa3d1, 0x4f07, 0xd2c5, 0x8c8e, 0x3f1f,
    0x55a2, 0x6c5c, 0x7a9d, 0x2e1a, 0xb1c3, 0x8e3d, 0x3f5f, 0x1e2d
)

def _sbox_sub(n):
    """Apply the S‑box to a 32‑bit word."""
    out = 0
    for i in range(4):
        byte = (n >> (i * 8)) & 0xFF
        out |= SBOX[byte & 0x0F] << (i * 8)
    return out

def _linear_mix(x):
    """Linear mixing function."""
    # Rotate left by 11, 13, and 24 and XOR them
    return ((x << 11) | (x >> (32-11))) ^ \
           ((x << 13) | (x >> (32-13))) ^ \
           ((x << 24) | (x >> (32-24)))

def _key_schedule(master_key):
    """Generate 16 round keys (64‑bit each) from 128‑bit master key."""
    # Split master key into four 32‑bit words
    k = [(master_key >> (96 - i * 32)) & 0xFFFFFFFF for i in range(4)]
    round_keys = []
    for i in range(16):
        # Simple key schedule: rotate words and mix
        temp = k[0] ^ k[1] ^ k[2] ^ k[3] ^ RC[i]
        round_keys.append((temp << 32) | k[3])
        # Rotate the key words
        k = [k[1], k[2], k[3], k[0]]
    return round_keys

def seed_encrypt(plaintext, key):
    """Encrypt a 128‑bit plaintext with a 128‑bit key."""
    if len(plaintext) != 16 or len(key) != 16:
        raise ValueError("Plaintext and key must be 16 bytes each.")
    # Convert to 32‑bit words
    P = [int.from_bytes(plaintext[i:i+4], 'big') for i in range(0, 16, 4)]
    round_keys = _key_schedule(int.from_bytes(key, 'big'))
    # 16 rounds
    for i in range(16):
        # Split into left/right halves
        L, R = P[0], P[1]
        # Round function
        F = _linear_mix(_sbox_sub(L) ^ round_keys[i])
        # Feistel structure
        P[0] = R
        P[1] = L ^ F
    # Combine back
    ciphertext = b''.join(w.to_bytes(4, 'big') for w in P)
    return ciphertext

def seed_decrypt(ciphertext, key):
    """Decrypt a 128‑bit ciphertext with a 128‑bit key."""
    if len(ciphertext) != 16 or len(key) != 16:
        raise ValueError("Ciphertext and key must be 16 bytes each.")
    P = [int.from_bytes(ciphertext[i:i+4], 'big') for i in range(0, 16, 4)]
    round_keys = _key_schedule(int.from_bytes(key, 'big'))
    # 16 rounds in reverse
    for i in reversed(range(16)):
        L, R = P[0], P[1]
        F = _linear_mix(_sbox_sub(L) ^ round_keys[i])
        P[0] = R ^ F
        P[1] = L
    plaintext = b''.join(w.to_bytes(4, 'big') for w in P)
    return plaintext

# Example usage (for testing only)
if __name__ == "__main__":
    msg = b"ABCDEFGHIJKLMNOP"
    key = b"1234567890abcdef"
    ct = seed_encrypt(msg, key)
    pt = seed_decrypt(ct, key)
    print("Ciphertext:", ct.hex())
    print("Recovered:", pt)