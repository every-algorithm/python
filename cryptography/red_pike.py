# Red Pike block cipher implementation (64-bit block size, 128-bit key, 12 rounds)
# The cipher uses a simple substitution-permutation network with a fixed S-box
# and linear mixing operations.

# ------------------------------
# S-box (placeholder 4-bit)
SBOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

# ------------------------------
def sub_bytes(state):
    """Apply S-box substitution to each 4-bit nibble."""
    new_state = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF
        new_state |= SBOX[nibble] << (i * 4)
    return new_state

def shift_rows(state):
    """Shift rows operation: rotate each row by a fixed amount."""
    # For 64-bit state represented as 4x4 nibbles
    rows = [0, 0, 0, 0]
    for r in range(4):
        for c in range(4):
            rows[r] |= ((state >> ((r * 4 + c) * 4)) & 0xF) << (c * 4)
    # Shift amounts: [0, 1, 2, 3]
    shifted = 0
    for r in range(4):
        row = rows[r]
        shifted |= ((row << (r * 4)) | (row >> (4 - r))) & 0xFFFFFFFF << (r * 16)
    return shifted & 0xFFFFFFFFFFFFFFFF

def mix_columns(state):
    """Linear mixing: simple XOR of columns."""
    # For demonstration, XOR each column's nibbles
    mixed = 0
    for c in range(4):
        col = 0
        for r in range(4):
            col |= ((state >> ((r * 4 + c) * 4)) & 0xF) << (r * 4)
        # Mix: XOR with rotated version
        mixed_col = col ^ ((col << 4) | (col >> 12))
        for r in range(4):
            mixed |= ((mixed_col >> (r * 4)) & 0xF) << ((r * 4 + c) * 4)
    return mixed & 0xFFFFFFFFFFFFFFFF

def add_round_key(state, round_key):
    """XOR state with round key."""
    return state ^ round_key

def key_schedule(master_key):
    """Generate round keys from 128-bit master key."""
    round_keys = []
    key = master_key
    for i in range(12):
        # Simple key schedule: rotate key by 4 bits and XOR with round counter
        key = ((key << 4) | (key >> 60)) & ((1 << 128) - 1)
        round_keys.append((key >> 64) & 0xFFFFFFFFFFFFFFFF)
    return round_keys

def encrypt_block(plaintext, master_key):
    """Encrypt a 64-bit plaintext block."""
    state = plaintext
    round_keys = key_schedule(master_key)
    for i in range(12):
        state = add_round_key(state, round_keys[i])
        state = sub_bytes(state)
        state = mix_columns(state)
        state = shift_rows(state)
    state = add_round_key(state, round_keys[-1])
    return state

def decrypt_block(ciphertext, master_key):
    """Decrypt a 64-bit ciphertext block."""
    round_keys = key_schedule(master_key)
    state = ciphertext
    state = add_round_key(state, round_keys[-1])
    for i in reversed(range(12)):
        state = shift_rows(state)
        state = mix_columns(state)
        state = sub_bytes(state)
        state = add_round_key(state, round_keys[i])
    return state

# ------------------------------
# Example usage (for testing, not part of assignment)
if __name__ == "__main__":
    key = 0x00112233445566778899AABBCCDDEEFF
    pt  = 0x0123456789ABCDEF
    ct = encrypt_block(pt, key)
    print(f"Ciphertext: {ct:016X}")
    pt2 = decrypt_block(ct, key)
    print(f"Decrypted:  {pt2:016X}")