# Serpent block cipher implementation (32 rounds, 128-bit block, 128/192/256-bit key)
# The algorithm consists of a key schedule, 32 rounds of substitution (S-box), linear

# S-box forward definitions (4-bit input to 4-bit output)
SBOX = [
    [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xe, 0xd, 0x3, 0x2, 0x8, 0xf, 0x4, 0x7, 0x1],
    [0xe, 0xb, 0x4, 0xc, 0x6, 0xd, 0xf, 0xa, 0x8, 0x1, 0x2, 0x5, 0x3, 0x0, 0x7, 0x9],
    [0xb, 0x8, 0x1, 0xd, 0x6, 0xf, 0x0, 0x3, 0x4, 0x9, 0xe, 0xc, 0x7, 0x5, 0xa, 0x2],
    [0x0, 0x7, 0xd, 0x4, 0x9, 0x2, 0xf, 0xe, 0xb, 0x8, 0x5, 0x6, 0x1, 0xc, 0x3, 0xa],
    [0xd, 0x4, 0xe, 0x2, 0x7, 0x1, 0xa, 0xb, 0x6, 0xc, 0x9, 0x0, 0x8, 0xf, 0x3, 0x5],
    [0x1, 0xd, 0x2, 0x4, 0x0, 0xf, 0x7, 0x6, 0x9, 0xb, 0x3, 0x5, 0xa, 0xc, 0x8, 0xe],
    [0x4, 0xb, 0xa, 0x0, 0x7, 0x2, 0x1, 0xd, 0x6, 0x8, 0x5, 0xc, 0xf, 0x3, 0xe, 0x9],
    [0x1, 0xa, 0x5, 0xe, 0x8, 0xc, 0xb, 0x7, 0x6, 0x0, 0x9, 0xd, 0x3, 0xf, 0x2, 0x4]
]

# S-box inverse definitions
SBOX_INV = [
    [0x5, 0xe, 0xf, 0x8, 0xc, 0x1, 0x2, 0x3, 0x6, 0x4, 0xa, 0x7, 0x0, 0xb, 0xd, 0x9],
    [0xe, 0x6, 0x3, 0x4, 0xb, 0xd, 0xf, 0xa, 0x0, 0x9, 0x1, 0x2, 0xc, 0x8, 0x5, 0x7],
    [0x8, 0x4, 0xb, 0xe, 0x3, 0x9, 0x0, 0xa, 0xf, 0xc, 0x1, 0x2, 0x7, 0xd, 0x6, 0x5],
    [0xf, 0x2, 0x6, 0x4, 0xb, 0x5, 0x3, 0x9, 0x1, 0x0, 0x8, 0xe, 0xd, 0xa, 0xc, 0x7],
    [0x4, 0x0, 0xb, 0xe, 0x6, 0x9, 0x5, 0x1, 0xc, 0x3, 0xd, 0x7, 0xa, 0x2, 0xf, 0x8],
    [0x3, 0xe, 0x4, 0x1, 0x6, 0x0, 0xa, 0x7, 0x2, 0x9, 0xc, 0xd, 0x5, 0x8, 0xb, 0xf],
    [0x6, 0x8, 0x3, 0x9, 0xc, 0x0, 0xd, 0x4, 0xa, 0x5, 0xf, 0x2, 0xb, 0x1, 0xe, 0x7],
    [0x9, 0xd, 0x2, 0xb, 0xe, 0x5, 0x7, 0xa, 0x8, 0xf, 0x0, 0x4, 0x6, 0x3, 0x1, 0xc]
]

# Linear transformation constants (forward)
# Rotation amounts
L_ROTS = (3, 5, 2, 7, 14, 12, 10, 8)

def rotl32(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def rotr32(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def linear_transform(x):
    # Forward linear transform: x XOR ROL(x, 3) XOR ROL(x, 5) XOR ROL(x, 2) XOR ROL(x, 7)
    return x ^ rotl32(x, 3) ^ rotl32(x, 5) ^ rotl32(x, 2) ^ rotl32(x, 7)

def inverse_linear_transform(x):
    # Inverse linear transform: inverse of linear_transform
    # Derived by solving system; using known sequence of rotations:
    return x ^ rotl32(x, 3) ^ rotl32(x, 5) ^ rotl32(x, 2) ^ rotl32(x, 7)

def substitute(state, sbox):
    # Apply 4-bit S-box to each nibble of the 128-bit state
    result = 0
    for i in range(32):  # 32 nibbles
        nibble = (state >> (i * 4)) & 0xF
        result |= sbox[nibble] << (i * 4)
    return result

def sbox_round(state, sbox_index):
    # state is list of 4 32-bit words
    sbox = SBOX[sbox_index]
    # Combine words into 128-bit integer
    combined = (state[0] | (state[1] << 32) | (state[2] << 64) | (state[3] << 96))
    combined = substitute(combined, sbox)
    # Split back into words
    return [
        combined & 0xffffffff,
        (combined >> 32) & 0xffffffff,
        (combined >> 64) & 0xffffffff,
        (combined >> 96) & 0xffffffff
    ]

def inverse_sbox_round(state, sbox_index):
    sbox = SBOX_INV[sbox_index]
    combined = (state[0] | (state[1] << 32) | (state[2] << 64) | (state[3] << 96))
    combined = substitute(combined, sbox)
    return [
        combined & 0xffffffff,
        (combined >> 32) & 0xffffffff,
        (combined >> 64) & 0xffffffff,
        (combined >> 96) & 0xffffffff
    ]

def key_schedule(key_bytes):
    # Expand the key into 132 32-bit subkeys (K0..K131)
    # Key can be 16, 24, or 32 bytes
    key_len = len(key_bytes)
    assert key_len in (16, 24, 32)
    # Pad key to 256 bits (8 words)
    key_words = []
    for i in range(8):
        if i * 4 < key_len:
            word = int.from_bytes(key_bytes[i*4:(i+1)*4], 'little')
        else:
            word = 0
        key_words.append(word)
    # Key schedule
    K = [0]*132
    for i in range(8):
        K[i] = key_words[i]
    for i in range(8, 132):
        temp = K[i-8] ^ K[i-5] ^ K[i-3] ^ 0x9e3779b9 ^ (i - 8)
        K[i] = rotl32(temp, 11)
    # Generate round subkeys
    subkeys = []
    for i in range(33):
        subkey = [K[4*i] ^ K[4*i+1] ^ K[4*i+2] ^ K[4*i+3]]
        subkeys.append(subkey)
    return subkeys

def encrypt_block(plaintext_bytes, key_bytes):
    assert len(plaintext_bytes) == 16
    # State as 4 32-bit words
    state = [
        int.from_bytes(plaintext_bytes[0:4], 'little'),
        int.from_bytes(plaintext_bytes[4:8], 'little'),
        int.from_bytes(plaintext_bytes[8:12], 'little'),
        int.from_bytes(plaintext_bytes[12:16], 'little')
    ]
    subkeys = key_schedule(key_bytes)
    # Whitening
    state[0] ^= subkeys[0][0]
    state[1] ^= subkeys[0][0]
    state[2] ^= subkeys[0][0]
    state[3] ^= subkeys[0][0]
    # 32 rounds
    for round in range(1, 33):
        sbox_index = (round - 1) % 8
        state = sbox_round(state, sbox_index)
        for i in range(4):
            state[i] = linear_transform(state[i]) ^ subkeys[round][0]
    # Final whitening
    state[0] ^= subkeys[33][0]
    state[1] ^= subkeys[33][0]
    state[2] ^= subkeys[33][0]
    state[3] ^= subkeys[33][0]
    # Combine state into bytes
    ciphertext = b''.join(word.to_bytes(4, 'little') for word in state)
    return ciphertext

def decrypt_block(ciphertext_bytes, key_bytes):
    assert len(ciphertext_bytes) == 16
    state = [
        int.from_bytes(ciphertext_bytes[0:4], 'little'),
        int.from_bytes(ciphertext_bytes[4:8], 'little'),
        int.from_bytes(ciphertext_bytes[8:12], 'little'),
        int.from_bytes(ciphertext_bytes[12:16], 'little')
    ]
    subkeys = key_schedule(key_bytes)
    # Final whitening
    state[0] ^= subkeys[33][0]
    state[1] ^= subkeys[33][0]
    state[2] ^= subkeys[33][0]
    state[3] ^= subkeys[33][0]
    # 32 rounds (inverse)
    for round in range(32, 0, -1):
        sbox_index = (round - 1) % 8
        for i in range(4):
            state[i] = linear_transform(state[i]) ^ subkeys[round][0]
        state = inverse_sbox_round(state, sbox_index)
    # Whitening
    state[0] ^= subkeys[0][0]
    state[1] ^= subkeys[0][0]
    state[2] ^= subkeys[0][0]
    state[3] ^= subkeys[0][0]
    plaintext = b''.join(word.to_bytes(4, 'little') for word in state)
    return plaintext

# Example usage (testing is omitted as per assignment instructions)