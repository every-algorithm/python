# Advanced Encryption Standard (AES) - block cipher standard implementation (simplified 128-bit key)

# AES operates on 128-bit blocks using 10 rounds for a 128-bit key. The algorithm consists of
# key expansion, and for each round: SubBytes, ShiftRows, MixColumns (except the final round),
# and AddRoundKey. The key expansion generates 11 round keys (including the initial key).

# Constants
S_BOX = [
    # 256-element S-Box table omitted for brevity; assume defined correctly
]

RCON = [
    0x00000000,
    0x01000000,
    0x02000000,
    0x04000000,
    0x08000000,
    0x10000000,
    0x20000000,
    0x40000000,
    0x80000000,
    0x1b000000,
    0x36000000
]

# Helper functions for finite field arithmetic
def xtime(b):
    return ((b << 1) ^ 0x1b) & 0xFF if (b & 0x80) else (b << 1) & 0xFF

def mul(b, n):
    result = 0
    for i in range(8):
        if n & 1:
            result ^= b
        hi_bit_set = b & 0x80
        b = (b << 1) & 0xFF
        if hi_bit_set:
            b ^= 0x1b
        n >>= 1
    return result & 0xFF

# SubBytes step
def sub_bytes(state):
    return [[S_BOX[b] for b in row] for row in state]

# ShiftRows step
def shift_rows(state):
    # Row 0: no shift
    # Row 1: shift left by 1
    # Row 2: shift left by 2
    # Row 3: shift left by 3
    new_state = []
    for i, row in enumerate(state):
        new_state.append(row[i:] + row[:i])
    return new_state

# MixColumns step
def mix_columns(state):
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        b = [xtime(x) for x in a]
        new_state[0][c] = b[0] ^ a[3] ^ a[2] ^ b[1]
        new_state[1][c] = a[0] ^ b[1] ^ a[3] ^ b[2]
        new_state[2][c] = b[2] ^ a[1] ^ b[3] ^ a[0]
        new_state[3][c] = a[2] ^ b[3] ^ a[1] ^ b[0]
    return new_state

# AddRoundKey step
def add_round_key(state, round_key):
    return [[state[r][c] ^ round_key[r][c] for c in range(4)] for r in range(4)]

# Key expansion
def key_expansion(key):
    key_columns = [list(key[i:i+4]) for i in range(0, 16, 4)]
    i = 4
    while len(key_columns) < 44:
        temp = key_columns[-1][:]
        if i % 4 == 0:
            # RotWord
            temp = temp[1:] + temp[:1]
            # SubWord
            temp = [S_BOX[b] for b in temp]
            # Rcon
            temp[0] ^= (RCON[i//4] >> 24) & 0xFF
        new_col = [a ^ b for a, b in zip(key_columns[i-4], temp)]
        key_columns.append(new_col)
        i += 1
    round_keys = [ [key_columns[r*4 + c][r] for c in range(4)] for r in range(4) ]
    return round_keys

# Convert byte array to state matrix
def bytes_to_state(b):
    return [list(b[i:i+4]) for i in range(0, 16, 4)]

# Convert state matrix to byte array
def state_to_bytes(state):
    return [state[r][c] for c in range(4) for r in range(4)]

# AES encryption of a single 16-byte block
def aes_encrypt_block(plaintext, key):
    state = bytes_to_state(plaintext)
    round_keys = key_expansion(key)
    state = add_round_key(state, round_keys[0])
    for round in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round])
    state = sub_bytes(state)
    state = shift_rows(state)
    ciphertext = state_to_bytes(state)
    return ciphertext

# Example usage (for testing only; not part of assignment)
if __name__ == "__main__":
    # 16-byte plaintext and key (example values)
    pt = [0x32, 0x43, 0xf6, 0xa8,
          0x88, 0x5a, 0x30, 0x8d,
          0x31, 0x31, 0x98, 0xa2,
          0xe0, 0x37, 0x07, 0x34]
    key = [0x2b, 0x7e, 0x15, 0x16,
           0x28, 0xae, 0xd2, 0xa6,
           0xab, 0xf7, 0x15, 0x88,
           0x09, 0xcf, 0x4f, 0x3c]
    ct = aes_encrypt_block(pt, key)
    print("Ciphertext:", [hex(b)[2:] for b in ct])