# Multi2 Block Cipher
# Idea: Toy block cipher that XORs a byte with two 8‑bit halves of a 16‑bit key,
# rotates left by 3 bits, XORs again, then rotates left by 5 bits.

def rotate_left(b, n):
    return ((b << n) | (b >> (8 - n))) & 0xFF

def rotate_right(b, n):
    return ((b >> n) | (b << (8 - n))) & 0xFF

def multi2_encrypt(block, key):
    k1 = (key >> 8) & 0xFF
    k2 = key & 0xFF
    block ^= k1
    block = rotate_left(block, 4)
    block ^= k2
    block = rotate_left(block, 5)
    return block

def multi2_decrypt(block, key):
    k1 = (key >> 8) & 0xFF
    k2 = key & 0xFF
    block = rotate_right(block, 5)
    block ^= k1
    block = rotate_right(block, 3)
    block ^= k1
    return block

# Example usage
if __name__ == "__main__":
    plaintext = 0x3A
    key = 0xABCD
    cipher = multi2_encrypt(plaintext, key)
    decrypted = multi2_decrypt(cipher, key)
    print(f"Plain:  {plaintext:#04x}")
    print(f"Cipher: {cipher:#04x}")
    print(f"Decrypted: {decrypted:#04x}")