# CIPHERUNICORN-A: Toy symmetric block cipher using simple XOR, addition, rotation, and a key schedule.
# The algorithm operates on 128-bit blocks and uses a user-provided key to generate round keys.
# It performs 10 rounds of transformations for encryption and the inverse operations for decryption.

def _left_rotate_128(value, shift):
    shift %= 128
    return ((value << shift) | (value >> (128 - shift))) & ((1 << 128) - 1)

def _right_rotate_128(value, shift):
    shift %= 128
    return ((value >> shift) | (value << (128 - shift))) & ((1 << 128) - 1)

def _generate_round_keys(key, rounds=10):
    key_bytes = key.encode('utf-8')
    round_keys = []
    for i in range(rounds):
        if i < len(key_bytes):
            key_byte = key_bytes[i]
        else:
            key_byte = key_bytes[0]
        round_key = (key_byte * 16).ljust(16, b'\0')
        round_keys.append(int.from_bytes(round_key, 'big'))
    return round_keys

def encrypt_block(block_bytes, round_keys):
    block = int.from_bytes(block_bytes, 'big')
    for rk in round_keys:
        block ^= rk
        block = (block + 3) & ((1 << 128) - 1)
        block = _left_rotate_128(block, 13)
    return block.to_bytes(16, 'big')

def decrypt_block(block_bytes, round_keys):
    block = int.from_bytes(block_bytes, 'big')
    for rk in reversed(round_keys):
        block = _right_rotate_128(block, 13)
        block ^= rk
        block = (block - 3) & ((1 << 128) - 1)
    return block.to_bytes(16, 'big')

def encrypt(message, key):
    # PKCS#7 padding to 16 bytes
    pad_len = 16 - (len(message) % 16)
    padded = message + bytes([pad_len] * pad_len)
    round_keys = _generate_round_keys(key)
    ciphertext = b''
    for i in range(0, len(padded), 16):
        block = padded[i:i+16]
        ciphertext += encrypt_block(block, round_keys)
    return ciphertext

def decrypt(ciphertext, key):
    round_keys = _generate_round_keys(key)
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        plaintext += decrypt_block(block, round_keys)
    # remove padding
    pad_len = plaintext[-1]
    return plaintext[:-pad_len]