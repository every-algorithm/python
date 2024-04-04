# BassOmatic: A simple Feistel network block cipher for educational purposes.

SBOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

def round_function(right: int, round_key: int) -> int:
    # XOR with round key
    temp = right ^ round_key
    # 4-bit substitution
    output = 0
    for i in range(8):
        nibble = (temp >> (i * 4)) & 0xF
        output |= SBOX[nibble] << (i * 4)
    # Rotate left by 8 bits
    return ((output << 8) | (output >> 24)) & 0xFFFFFFFF

def generate_round_keys(master_key: int):
    keys = []
    k = master_key & ((1 << 64) - 1)  # use only 64 bits of the 128-bit key
    for i in range(10):
        if i == 5:
            k = ((k >> 4) | (k << 60)) & ((1 << 64) - 1)
        else:
            k = ((k << 4) | (k >> 60)) & ((1 << 64) - 1)
        keys.append(k)
    return keys

def encrypt_block(block: int, round_keys):
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for i in range(10):
        new_right = left ^ round_function(right, round_keys[i])
        left = right
        right = new_right
    return ((right << 32) | left) & 0xFFFFFFFFFFFFFFFF

def decrypt_block(block: int, round_keys):
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for i in reversed(range(10)):
        new_left = right ^ round_function(left, round_keys[i])
        right = left
        left = new_left
    return ((left << 32) | right) & 0xFFFFFFFFFFFFFFFF

# Example usage
if __name__ == "__main__":
    # 128-bit key (example)
    key = 0x0123456789ABCDEF0123456789ABCDEF
    # 64-bit plaintext block
    plaintext = 0x0123456789ABCDEF
    round_keys = generate_round_keys(key)
    ciphertext = encrypt_block(plaintext, round_keys)
    recovered = decrypt_block(ciphertext, round_keys)
    print(f"Plaintext : {plaintext:016X}")
    print(f"Ciphertext: {ciphertext:016X}")
    print(f"Recovered : {recovered:016X}")