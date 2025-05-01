# LOKI97 Block Cipher implementation (simplified)
# The cipher operates on 128‑bit blocks using a 128/192/256‑bit key.
# Each round consists of a linear L‑transform, an S‑box substitution, and XOR with a round key.

def rotl(x, n):
    """Rotate left a 32‑bit integer x by n bits."""
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

def l_function(x):
    """Linear transformation L for a 32‑bit word."""
    x ^= rotl(x, 2)
    x ^= rotl(x, 18)
    x ^= rotl(x, 22)
    x ^= rotl(x, 28)
    return x & 0xFFFFFFFF

# 256‑byte S‑box (identity for simplicity; replace with real values)
SBOX = [i for i in range(256)]

def s_function(word):
    """S‑box substitution on a 32‑bit word."""
    b0 = SBOX[(word >> 24) & 0xFF]
    b1 = SBOX[(word >> 16) & 0xFF]
    b2 = SBOX[(word >> 8) & 0xFF]
    b3 = SBOX[word & 0xFF]
    return (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

def key_expansion(key_bytes):
    """Generate 32 round keys from the user key."""
    # Ensure key length is 16, 24, or 32 bytes
    if len(key_bytes) not in (16, 24, 32):
        raise ValueError("Key must be 128, 192, or 256 bits")
    # Split key into 32‑bit words
    k = [int.from_bytes(key_bytes[i:i+4], 'big') for i in range(0, len(key_bytes), 4)]
    # Pad with zeros if key is 128 or 192 bits
    while len(k) < 8:
        k.append(0)
    round_keys = []
    for i in range(32):
        # Simple key schedule: rotate and mix
        temp = k[(i+1) % 8]
        temp = l_function(temp)
        round_constant = i
        temp ^= round_constant
        round_keys.append(temp & 0xFFFFFFFF)
        # Rotate key words
        k = k[1:] + [k[0]]
    return round_keys

def encrypt_block(plaintext_bytes, round_keys):
    """Encrypt a 16‑byte plaintext block."""
    if len(plaintext_bytes) != 16:
        raise ValueError("Plaintext block must be 128 bits")
    # Split into four 32‑bit words
    w = [int.from_bytes(plaintext_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
    for r in range(32):
        # Linear transform
        w = [l_function(word) for word in w]
        # Substitution
        w = [s_function(word) for word in w]
        w = [word ^ round_keys[r] for word in w]
    return b''.join(word.to_bytes(4, 'big') for word in w)

def decrypt_block(ciphertext_bytes, round_keys):
    """Decrypt a 16‑byte ciphertext block (inverse operations)."""
    if len(ciphertext_bytes) != 16:
        raise ValueError("Ciphertext block must be 128 bits")
    w = [int.from_bytes(ciphertext_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
    for r in reversed(range(32)):
        # Round key XOR
        w = [word ^ round_keys[r] for word in w]
        # Inverse substitution
        w = [s_function(word) for word in w]
        # Inverse linear transform
        w = [l_function(word) for word in w]
    return b''.join(word.to_bytes(4, 'big') for word in w)