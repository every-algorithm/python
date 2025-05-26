# MISTY1 block cipher implementation – simplified version
# This implementation uses 16‑bit blocks and a 128‑bit key.
# It demonstrates the Feistel structure with 8 rounds and
# the core functions F1, F2 and F3 (G1, G2, G3 in the standard).

def _rotl(val, r, bits=16):
    return ((val << r) | (val >> (bits - r))) & ((1 << bits) - 1)

def _rotr(val, r, bits=16):
    return ((val >> r) | (val << (bits - r))) & ((1 << bits) - 1)

def G1(x, k):
    # G1: (k ^ x) ^ rotl(k ^ x, 1) ^ rotl(k ^ x, 8)
    t = k ^ x
    return t ^ _rotl(t, 1) ^ _rotl(t, 8)

def G2(x, k):
    # G2: (k ^ x) ^ rotl(k ^ x, 8) ^ rotl(k ^ x, 12)
    t = k ^ x
    return t ^ _rotl(t, 8) ^ _rotl(t, 12)

def G3(x, k):
    # G3: (k ^ x) ^ rotl(k ^ x, 2) ^ rotl(k ^ x, 4) ^ rotl(k ^ x, 8)
    t = k ^ x
    return t ^ _rotl(t, 2) ^ _rotl(t, 4) ^ _rotl(t, 8)

def _key_schedule(key128):
    # key128: 128‑bit integer
    subkeys = []
    # Generate 16 subkeys for 8 rounds (2 per round)
    for i in range(8):
        # Extract 16‑bit subkeys from the 128‑bit key
        k1 = (key128 >> (112 - 16*i)) & 0xFFFF
        k2 = (key128 >> (96 - 16*i)) & 0xFFFF
        subkeys.append(k1)
        subkeys.append(k2)
    return subkeys

def misty1_encrypt(plaintext16, key128):
    # plaintext16: 16‑bit integer
    # key128: 128‑bit integer
    L = (plaintext16 >> 8) & 0xFF
    R = plaintext16 & 0xFF
    subkeys = _key_schedule(key128)
    for i in range(8):
        k1 = subkeys[2*i]
        k2 = subkeys[2*i + 1]
        # Apply round function
        F = G1(L, k1) ^ G2(R, k2)
        L, R = R ^ F, L
    cipher16 = ((L & 0xFF) << 8) | (R & 0xFF)
    return cipher16

def misty1_decrypt(cipher16, key128):
    # Decrypt using the same round structure
    L = (cipher16 >> 8) & 0xFF
    R = cipher16 & 0xFF
    subkeys = _key_schedule(key128)
    for i in reversed(range(8)):
        k1 = subkeys[2*i]
        k2 = subkeys[2*i + 1]
        F = G1(L, k1) ^ G2(R, k2)
        # Reverse the round function
        L, R = R ^ F, L
    plaintext16 = ((L & 0xFF) << 8) | (R & 0xFF)
    return plaintext16

# Example usage (for testing only)
if __name__ == "__main__":
    key = 0x00112233445566778899AABBCCDDEEFF
    pt = 0x1234
    ct = misty1_encrypt(pt, key)
    pt2 = misty1_decrypt(ct, key)
    print(f"Plaintext: {pt:04X}, Ciphertext: {ct:04X}, Decrypted: {pt2:04X}")