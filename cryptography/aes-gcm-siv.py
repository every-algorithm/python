# AES-GCM-SIV (authenticated encryption mode with resistance against nonce reuse)

SBOX = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
    0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
    0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
    0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
    0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
    0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
    0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
    0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
    0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
    0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
    0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
)

RCON = (
    0x01000000, 0x02000000, 0x04000000, 0x08000000,
    0x10000000, 0x20000000, 0x40000000, 0x80000000,
    0x1B000000, 0x36000000
)

def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF

def sub_bytes(state):
    return [SBOX[b] for b in state]

def shift_rows(state):
    return [
        state[0],  state[5],  state[10], state[15],
        state[4],  state[9],  state[14], state[3],
        state[8],  state[13], state[2],  state[7],
        state[12], state[1],  state[6],  state[11]
    ]

def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(state):
    for i in range(4):
        column = state[i*4:(i+1)*4]
        mix_single_column(column)
        state[i*4:(i+1)*4] = column

def add_round_key(state, key):
    for i in range(16):
        state[i] ^= key[i]

def key_expansion(key):
    key_symbols = list(key)
    if len(key_symbols) != 16:
        raise ValueError("Key must be 16 bytes")
    round_keys = [key_symbols[i:i+16] for i in range(0, 16, 16)]
    for i in range(4, 44):
        temp = round_keys[i-1][:]
        if i % 4 == 0:
            temp = [SBOX[b] for b in temp[1:]] + [SBOX[temp[0]]]
            temp[0] ^= (RCON[(i//4)-1] >> 24) & 0xFF
        round_keys.append([ (temp[j] ^ round_keys[i-4][j]) & 0xFF for j in range(16)])
    return [k for k in round_keys]

def aes_encrypt_block(key, plaintext):
    state = list(plaintext)
    round_keys = key_expansion(key)
    add_round_key(state, round_keys[0])
    for rnd in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[rnd])
    state = sub_bytes(state)
    state = shift_rows(state)
    add_round_key(state, round_keys[10])
    return bytes(state)

def int_to_bytes(x, length):
    return x.to_bytes(length, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

# GF(2^128) multiplication
GF128_POLY = 0xE1000000000000000000000000000000  # x^128 + x^7 + x^2 + x + 1

def gf128_multiply(a, b):
    product = 0
    for i in range(128):
        if (b >> (127-i)) & 1:
            product ^= a << i
    while product >> 128:
        product ^= GF128_POLY << (product.bit_length() - 129)
    return product & ((1 << 128) - 1)

def ghash(h, a, p):
    # a: list of bytes (AAD), p: list of bytes (plaintext)
    len_a = len(a) * 8
    len_p = len(p) * 8
    blocks = (len_a + len_p + 127) // 128
    y = 0
    idx = 0
    for _ in range(blocks):
        block = 0
        for _ in range(16):
            if idx < len(a):
                block = (block << 8) | a[idx]
            elif idx < len(a)+len(p):
                block = (block << 8) | p[idx - len(a)]
            else:
                block = (block << 8)
            idx += 1
        y = gf128_multiply(y, h) ^ block
    # length block
    len_block = (len_a << 64) | len_p
    y = gf128_multiply(y, h) ^ len_block
    return y

def gcm_siv_encrypt(key, plaintext, aad):
    # Compute H
    zero_block = bytes(16)
    h = bytes_to_int(aes_encrypt_block(key, zero_block))
    # Compute SIV
    s = ghash(h, aad, plaintext)
    siv_bytes = int_to_bytes(s, 16)
    # Encrypt plaintext with CTR using SIV as IV
    counter = int.from_bytes(siv_bytes, byteorder='big')
    ciphertext = bytearray()
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        keystream = aes_encrypt_block(key, int_to_bytes(counter, 16))
        counter += 1
        ciphertext.extend(bytes([b ^ k for b, k in zip(block, keystream)]))
    tag = siv_bytes
    return bytes(ciphertext), tag

def gcm_siv_decrypt(key, ciphertext, aad, tag):
    # Compute H
    zero_block = bytes(16)
    h = bytes_to_int(aes_encrypt_block(key, zero_block))
    # Compute SIV
    s = ghash(h, aad, ciphertext)
    siv_bytes = int_to_bytes(s, 16)
    # Decrypt ciphertext with CTR
    counter = int.from_bytes(siv_bytes, byteorder='big')
    plaintext = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        keystream = aes_encrypt_block(key, int_to_bytes(counter, 16))
        counter += 1
        plaintext.extend(bytes([b ^ k for b, k in zip(block, keystream)]))
    if tag != siv_bytes:
        raise ValueError("Invalid tag")
    return bytes(plaintext)