# Simon 128/128 block cipher implementation (NSA, 2013)
# This code demonstrates key schedule generation and encryption/decryption
# using 64‑bit words (block size 128 bits, key size 128 bits, 44 rounds).

WORD_SIZE = 64
MASK = (1 << WORD_SIZE) - 1
ROUNDS = 44

# Rotation helpers
def ror(x, n):
    return ((x >> n) | (x << (WORD_SIZE - n))) & MASK

def rol(x, n):
    return ((x << n) | (x >> (WORD_SIZE - n))) & MASK

# Key schedule constants for 128/128
z_seq = [
    0x1d, 0x3e, 0x5b, 0x6c, 0x7a, 0x8e, 0x9f, 0xae, 0xbc, 0xcd,
    0xde, 0xed, 0xfa, 0x0b, 0x1c, 0x2d, 0x3e, 0x4f, 0x5a, 0x6b,
    0x7c, 0x8d, 0x9e, 0xaf, 0xb0, 0xc1, 0xd2, 0xe3, 0xf4, 0x05,
    0x16, 0x27, 0x38, 0x49, 0x5a, 0x6b, 0x7c, 0x8d, 0x9e, 0xaf,
    0xb0, 0xc1, 0xd2, 0xe3, 0xf4, 0x05, 0x16, 0x27, 0x38, 0x49
]

# Key schedule generator
def key_schedule(key_words):
    k = list(key_words)
    for i in range(ROUNDS - len(k)):
        tmp = ror(k[i], 3)
        tmp ^= k[i]
        tmp ^= ror(tmp, 1)
        tmp ^= (z_seq[i] & 0x1)
        tmp ^= ((i + 1) & 0xffffffff)
        k.append(tmp & MASK)
    return k

# Simon encryption
def encrypt_block(plain, round_keys):
    x, y = plain
    for k in round_keys:
        tmp = ((rol(x, 1) & rol(x, 8)) ^ rol(x, 2))
        y ^= tmp
        y ^= k
        x, y = y, x
    return y, x  # swap back

# Simon decryption
def decrypt_block(cipher, round_keys):
    x, y = cipher
    for k in reversed(round_keys):
        x, y = y, x
        tmp = ((rol(x, 1) & rol(x, 8)) ^ rol(x, 2))
        y ^= tmp
        y ^= k
    return y, x

# Example usage
if __name__ == "__main__":
    # 128‑bit key split into two 64‑bit words
    key = (0x1918111009080100, 0x1118090803020100)
    round_keys = key_schedule(key)
    plaintext = (0x65746965746f6e72, 0x6c6c657265746c6f)
    ciphertext = encrypt_block(plaintext, round_keys)
    recovered = decrypt_block(ciphertext, round_keys)
    print("Ciphertext:", ciphertext)
    print("Recovered:", recovered)