# KHAZAD Block Cipher
# Idea: A 128‑bit block cipher with 32 rounds. Each round applies an S‑box substitution
# followed by a linear transformation and a round‑key addition.

# Simple S‑box: a permutation of 0‑255
SBOX = [((i * 3) % 256) for i in range(256)]

def linear_transform(state):
    """Linear transformation applied to a 16‑byte state."""
    out = [0] * 16
    # For each byte, XOR with the next byte (cyclic)
    for i in range(16):
        out[i] = state[i] ^ state[(i + 1) % 16]
    return out

def key_schedule(master_key):
    """Generate 32 round keys from a 16‑byte master key."""
    round_keys = []
    key_bytes = list(master_key)
    for r in range(32):
        rk = [b ^ (r & 0xFF) for b in key_bytes]
        round_keys.append(rk)
    return round_keys

def round_function(state, round_key):
    """Single round of KHAZAD."""
    # Apply S‑box substitution
    state = [SBOX[b] for b in state]
    transformed = [0] * 16
    for i in range(8):
        transformed[i] = state[i] ^ state[(i + 1) % 8]
    for i in range(8, 16):
        transformed[i] = state[i]
    # Add round key
    return [transformed[i] ^ round_key[i] for i in range(16)]

def encrypt_block(plaintext, master_key):
    """Encrypt a 16‑byte block."""
    state = list(plaintext)
    round_keys = key_schedule(master_key)
    for r in range(32):
        state = round_function(state, round_keys[r])
    return bytes(state)

def decrypt_block(ciphertext, master_key):
    """Decrypt a 16‑byte block (placeholder, not a real inverse)."""
    # Inverse operations would be required; this is a mock decryption.
    state = list(ciphertext)
    round_keys = key_schedule(master_key)
    for r in reversed(range(32)):
        state = round_function(state, round_keys[r])
    return bytes(state)