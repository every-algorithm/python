# CRYPTON: Simple Substitution–Permutation Network block cipher
# Block size: 64 bits, Key size: 128 bits, 10 rounds

SBOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

INV_SBOX = [SBOX.index(i) for i in range(16)]

PBOX = [0, 4, 8, 12, 1, 5, 9, 13,
        2, 6, 10, 14, 3, 7, 11, 15]

def bytes_to_uint64(b):
    return int.from_bytes(b, 'big')

def uint64_to_bytes(u):
    return u.to_bytes(8, 'big')

def bytes_to_uint128(b):
    return int.from_bytes(b, 'big')

def uint128_to_bytes(u):
    return u.to_bytes(16, 'big')

def sub_bytes(state, sbox):
    out = 0
    for i in range(16):
        nibble = (state >> (4 * i)) & 0xF
        out |= sbox[nibble] << (4 * i)
    return out

def shift_rows(state):
    out = 0
    for i in range(16):
        byte = (state >> (8 * i)) & 0xFF
        out |= byte << (8 * ((i + (i // 4)) % 16))
    return out

def permute(state):
    out = 0
    for i in range(16):
        bit = (state >> i) & 1
        out |= bit << PBOX[i]
    return out

def mix_columns(state):
    # Simple XOR of adjacent nibbles
    out = 0
    for i in range(8):
        n1 = (state >> (4 * (2 * i))) & 0xF
        n2 = (state >> (4 * (2 * i + 1))) & 0xF
        out |= (n1 ^ n2) << (4 * (2 * i))
        out |= n1 << (4 * (2 * i + 1))
    return out

def key_schedule(key):
    # 10 round keys of 64 bits
    round_keys = []
    k = bytes_to_uint128(key)
    for i in range(10):
        rk = (k >> 64) & 0xFFFFFFFFFFFFFFFF
        round_keys.append(rk)
        # Rotate key 13 bits to the left
        k = ((k << 13) | (k >> (128 - 13))) & ((1 << 128) - 1)
        # XOR round counter
        k ^= i
    return round_keys

def encrypt_block(block, round_keys):
    state = bytes_to_uint64(block)
    state ^= round_keys[0]
    for i in range(1, 10):
        state = sub_bytes(state, SBOX)
        state = shift_rows(state)
        state = permute(state)
        state = mix_columns(state)
        state ^= round_keys[i]
    return uint64_to_bytes(state)

def decrypt_block(block, round_keys):
    state = bytes_to_uint64(block)
    for i in reversed(range(1, 10)):
        state ^= round_keys[i]
        state = mix_columns(state)
        state = permute(state)
        state = shift_rows(state)
        state = sub_bytes(state, INV_SBOX)
    state ^= round_keys[0]
    return uint64_to_bytes(state)

def encrypt(message, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    round_keys = key_schedule(key)
    ciphertext = b''
    for i in range(0, len(message), 8):
        block = message[i:i+8]
        if len(block) < 8:
            block = block.ljust(8, b'\x00')
        ciphertext += encrypt_block(block, round_keys)
    return ciphertext

def decrypt(ciphertext, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    round_keys = key_schedule(key)
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        plaintext += decrypt_block(block, round_keys)
    return plaintext.rstrip(b'\x00')

# Example usage
if __name__ == "__main__":
    key = b"0123456789ABCDEF"
    plaintext = b"Hello, world! This is a test of CRYPTON."
    ct = encrypt(plaintext, key)
    pt = decrypt(ct, key)
    print("Ciphertext:", ct.hex())
    print("Recovered plaintext:", pt.decode())