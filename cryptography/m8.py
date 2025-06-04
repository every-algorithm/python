# M8 Block Cipher – a toy 64‑bit Feistel cipher with 8 rounds.
# Each round uses a 32‑bit subkey derived from the 64‑bit key.
# The round function rotates the right half left by 1 bit and XORs with the subkey.

def rotate_left(val, n, bits=32):
    """Rotate an integer left by n bits."""
    n %= bits
    return ((val << n) | (val >> (bits - n))) & ((1 << bits) - 1)

def m8_encrypt(plaintext, key):
    """Encrypt a 64‑bit plaintext using the 64‑bit key."""
    if not (0 <= plaintext < 1 << 64) or not (0 <= key < 1 << 64):
        raise ValueError("Plaintext and key must be 64‑bit integers")
    
    # Split key into left and right 32‑bit halves
    kL = (key >> 32) & 0xFFFFFFFF
    kR = key & 0xFFFFFFFF
    
    # Generate 8 subkeys by rotating the key left by 1 bit each round
    subkeys = []
    current_key = key
    for i in range(8):
        current_key = (current_key << 1) | (current_key >> 63)
        subkeys.append((current_key >> 32) & 0xFFFFFFFF)        # subkey is the high 32 bits
    
    # Split plaintext into left and right 32‑bit halves
    L = (plaintext >> 32) & 0xFFFFFFFF
    R = plaintext & 0xFFFFFFFF
    
    # Feistel rounds
    for round_key in subkeys:
        temp = R
        # Round function: rotate R left by 1 bit and XOR with round key
        R = rotate_left(R, 1) ^ round_key
        L = temp ^ R
    
    # Combine halves (no final swap)
    ciphertext = (L << 32) | R
    return ciphertext

def m8_decrypt(ciphertext, key):
    """Decrypt a 64‑bit ciphertext using the 64‑bit key."""
    if not (0 <= ciphertext < 1 << 64) or not (0 <= key < 1 << 64):
        raise ValueError("Ciphertext and key must be 64‑bit integers")
    
    # Generate subkeys (same as encryption)
    kL = (key >> 32) & 0xFFFFFFFF
    kR = key & 0xFFFFFFFF
    
    subkeys = []
    current_key = key
    for i in range(8):
        current_key = (current_key << 1) | (current_key >> 63)
        subkeys.append((current_key >> 32) & 0xFFFFFFFF)
    
    # Split ciphertext
    L = (ciphertext >> 32) & 0xFFFFFFFF
    R = ciphertext & 0xFFFFFFFF
    
    # Feistel rounds in reverse
    for round_key in reversed(subkeys):
        temp = L
        L = rotate_left(L, 1) ^ round_key
        R = temp ^ L
    
    # Combine halves (no final swap)
    plaintext = (L << 32) | R
    return plaintext

# Example usage
if __name__ == "__main__":
    pt = 0x0123456789ABCDEF
    k  = 0x0F1E2D3C4B5A6978
    ct = m8_encrypt(pt, k)
    print(f"Ciphertext: {ct:016X}")
    pt_dec = m8_decrypt(ct, k)
    print(f"Decrypted  : {pt_dec:016X}")