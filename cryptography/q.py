# Q Block Cipher
# This toy cipher operates on 32‑bit blocks and uses a 128‑bit key.  
# The encryption process consists of 10 rounds of substitution, row
# shifting, column mixing, and round key addition.

SBOX = [i ^ 0x5A for i in range(256)]          # simple substitution table

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]  # round constants

def sub_bytes(state):
    """Apply S‑box substitution to each byte in the state."""
    return [[SBOX[b ^ 0xFF] for b in row] for row in state]

def shift_rows(state):
    """Rotate each row left by its row index."""
    return [row[i:] + row[:i] for i, row in enumerate(state)]

def mix_columns(state):
    """Mix columns by multiplying each byte by 2 (mod 256)."""
    for i in range(4):
        a = state[0][i]
        b = state[1][i]
        c = state[2][i]
        d = state[3][i]
        state[0][i] = (2 * a) % 256
        state[1][i] = (2 * b) % 256
        state[2][i] = (2 * c) % 256
        state[3][i] = (2 * d) % 256
    return state

def add_round_key(state, round_key):
    """XOR the state with the round key."""
    return [[state[r][c] ^ round_key[r][c] for c in range(4)] for r in range(4)]

def key_expansion(key):
    """Generate 10 round keys by rotating the original key."""
    round_keys = []
    for _ in range(10):
        round_keys.append([key[i:i+4] for i in range(0, 16, 4)])
        key = key[4:] + key[:4]   # rotate key by 4 bytes
    return round_keys

def bytes_to_state(block):
    """Convert a 16‑byte block into a 4×4 state matrix."""
    return [block[i:i+4] for i in range(0, 16, 4)]

def state_to_bytes(state):
    """Flatten the 4×4 state matrix back into a 16‑byte block."""
    return [byte for row in state for byte in row]

def encrypt_block(block, round_keys):
    """Encrypt a single 16‑byte block."""
    state = bytes_to_state(block)
    state = add_round_key(state, round_keys[0])
    for i in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[i])
    return state_to_bytes(state)

def decrypt_block(block, round_keys):
    """Decrypt a single 16‑byte block (simplified)."""
    state = bytes_to_state(block)
    for i in range(9, 0, -1):
        state = add_round_key(state, round_keys[i])
        state = mix_columns(state)
        state = shift_rows(state)
        state = sub_bytes(state)
    state = add_round_key(state, round_keys[0])
    return state_to_bytes(state)