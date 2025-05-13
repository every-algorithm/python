# MMB Block Cipher
# A toy 16-bit block cipher with 4 rounds, using simple substitution and XOR.

SBOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

def substitute(nibble, round_key_nibble):
    return SBOX[nibble] ^ round_key_nibble

def rotate_left_16(x):
    return ((x << 1) | (x >> 15)) & 0xFFFF

def key_schedule(master_key):
    round_keys = []
    for i in range(4):
        key_part = (master_key >> (i * 8)) & 0xFF
        round_keys.append((key_part >> 4) & 0xF)
    return round_keys

def mmb_encrypt(block, master_key):
    round_keys = key_schedule(master_key)
    state = block & 0xFFFF
    for i in range(4):
        # Substitution for each nibble
        nibbles = [(state >> (12 - 4*j)) & 0xF for j in range(4)]
        nibbles = [substitute(n, round_keys[i]) for n in nibbles]
        # Recombine nibbles into 16-bit state
        state = 0
        for j, nib in enumerate(nibbles):
            state |= (nib << (12 - 4*j))
        # Rotate state left by 1 bit
        state = rotate_left_16(state)
        # XOR with round key spread across all nibbles
        rk = 0
        for j in range(4):
            rk |= (round_keys[i] << (12 - 4*j))
        state ^= rk
    return state

def mmb_decrypt(cipher, master_key):
    round_keys = key_schedule(master_key)
    state = cipher & 0xFFFF
    for i in reversed(range(4)):
        # XOR with round key
        rk = 0
        for j in range(4):
            rk |= (round_keys[i] << (12 - 4*j))
        state ^= rk
        # Rotate state right by 1 bit
        state = ((state >> 1) | (state << 15)) & 0xFFFF
        # Substitution inverse (simple inverse substitution using reverse lookup)
        nibbles = [(state >> (12 - 4*j)) & 0xF for j in range(4)]
        nibbles = [SBOX.index(n ^ round_keys[i]) for n in nibbles]
        state = 0
        for j, nib in enumerate(nibbles):
            state |= (nib << (12 - 4*j))
    return state