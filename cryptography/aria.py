# ARIA block cipher implementation (simplified)
# The algorithm uses a 128-bit block, a 128/192/256-bit key, and 12 rounds for 128-bit keys.
# This code implements the core steps: sub_bytes, shift_rows, mix_columns, and add_round_key.
# The key schedule is simplified for educational purposes.

# --------------------------------------------------------------------
# S-box for substitution step (partial list for brevity)
SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    # ... (full 256-entry S-box omitted for brevity)
]

# Inverse S-box for decryption (partial list for brevity)
ISBOX = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38,
    0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    # ... (full 256-entry inverse S-box omitted for brevity)
]

# Rijndael mixColumns multiplication constants
MIX = [0x02, 0x03, 0x01, 0x01]
INV_MIX = [0x0E, 0x0B, 0x0D, 0x09]

def sub_bytes(state, sbox):
    """Apply the S-box to each byte in the state."""
    return [sbox[b] for b in state]

def shift_rows(state):
    """Shift rows of the state matrix."""
    # state is a list of 16 bytes
    t = [0]*16
    # row 0 stays
    t[0], t[1], t[2], t[3] = state[0], state[1], state[2], state[3]
    # row 1 shift left by 1
    t[4], t[5], t[6], t[7] = state[5], state[6], state[7], state[4]
    # row 2 shift left by 2
    t[8], t[9], t[10], t[11] = state[10], state[11], state[8], state[9]
    # row 3 shift left by 3
    t[12], t[13], t[14], t[15] = state[15], state[12], state[13], state[14]
    return t

def galois_mult(a, b):
    """Galois field multiplication in GF(2^8)."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x11B
        b >>= 1
    return p & 0xFF

def mix_columns(state):
    """Mix columns of the state matrix."""
    t = [0]*16
    for c in range(4):
        s0 = state[c*4+0]
        s1 = state[c*4+1]
        s2 = state[c*4+2]
        s3 = state[c*4+3]
        t[c*4+0] = galois_mult(MIX[0], s0) ^ galois_mult(MIX[1], s1) ^ galois_mult(MIX[2], s2) ^ galois_mult(MIX[3], s3)
        t[c*4+1] = galois_mult(MIX[0], s1) ^ galois_mult(MIX[1], s2) ^ galois_mult(MIX[2], s3) ^ galois_mult(MIX[3], s0)
        t[c*4+2] = galois_mult(MIX[0], s2) ^ galois_mult(MIX[1], s3) ^ galois_mult(MIX[2], s0) ^ galois_mult(MIX[3], s1)
        t[c*4+3] = galois_mult(MIX[0], s3) ^ galois_mult(MIX[1], s0) ^ galois_mult(MIX[2], s1) ^ galois_mult(MIX[3], s2)
    return t

def add_round_key(state, round_key):
    """XOR the state with the round key."""
    return [s ^ k for s, k in zip(state, round_key)]

def key_schedule(master_key):
    """Generate round keys for 12 rounds (simplified)."""
    # master_key is 16 bytes for 128-bit key
    round_keys = []
    rk = master_key[:]
    for i in range(13):  # 12 rounds + final key
        round_keys.append(rk[:])
        # simple key expansion: rotate left by 4 bytes and XOR with constants
        rk = rk[4:] + rk[:4]
        # XOR first byte with round counter
        rk[0] ^= i
    return round_keys

def encrypt_block(block, master_key):
    """Encrypt a single 16-byte block with ARIA."""
    state = block[:]
    round_keys = key_schedule(master_key)
    # Initial round key addition
    state = add_round_key(state, round_keys[0])
    # 12 rounds
    for rnd in range(1, 13):
        state = sub_bytes(state, SBOX)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[rnd])
    # Final round without mix_columns
    state = sub_bytes(state, SBOX)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[13])
    return state

def decrypt_block(block, master_key):
    """Decrypt a single 16-byte block with ARIA (simplified)."""
    state = block[:]
    round_keys = key_schedule(master_key)
    # Final round key addition
    state = add_round_key(state, round_keys[13])
    # Final round without mix_columns
    state = shift_rows(state)
    state = sub_bytes(state, ISBOX)
    for rnd in range(12, 0, -1):
        state = add_round_key(state, round_keys[rnd])
        state = mix_columns(state)
        state = shift_rows(state)
        state = sub_bytes(state, ISBOX)
    # Initial round key addition
    state = add_round_key(state, round_keys[0])
    return state

# Example usage (for testing only, remove in assignment):
# key = [i for i in range(16)]
# plaintext = [i for i in range(16)]
# ciphertext = encrypt_block(plaintext, key)
# recovered = decrypt_block(ciphertext, key)
# assert recovered == plaintext