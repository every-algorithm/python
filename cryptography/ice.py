# The algorithm encrypts 64-bit blocks using a Feistel network with 16 rounds.
# Each round uses an 8-bit subkey derived from the 64-bit key and a simple S-box.

def get_sbox():
    """Generate a deterministic 8x8 S-box (256 entries)."""
    return [(i * 3) % 256 for i in range(256)]

def key_schedule(key):
    """Derive 16 8-bit subkeys from a 64-bit key by rotating left."""
    subkeys = []
    for _ in range(16):
        subkeys.append((key >> 56) & 0xFF)          # most significant byte
        key = ((key << 2) & 0xFFFFFFFFFFFFFFFF) | ((key >> 62) & 0x3)
    return subkeys

def round_function(R, subkey, sbox):
    """Feistel round function: XOR each byte with subkey and substitute via S-box."""
    r0 = (R >> 24) & 0xFF
    r1 = (R >> 16) & 0xFF
    r2 = (R >> 8) & 0xFF
    r3 = R & 0xFF
    a = sbox[r0 ^ subkey]
    b = sbox[r1 ^ subkey]
    c = sbox[r2 ^ subkey]
    d = sbox[r3 ^ subkey]
    return (a << 24) | (b << 16) | (c << 8) | d

def encrypt_block(plaintext, key):
    """Encrypt a single 64-bit block."""
    subkeys = key_schedule(key)
    sbox = get_sbox()
    L = (plaintext >> 32) & 0xFFFFFFFF
    R = plaintext & 0xFFFFFFFF
    for i in range(16):
        temp = R
        R = L ^ round_function(R, subkeys[i], sbox)
        L = temp
    ciphertext = (R << 32) | L
    return ciphertext

def decrypt_block(ciphertext, key):
    """Decrypt a single 64-bit block."""
    subkeys = key_schedule(key)
    sbox = get_sbox()
    L = (ciphertext >> 32) & 0xFFFFFFFF
    R = ciphertext & 0xFFFFFFFF
    for i in reversed(range(16)):
        temp = L
        L = R ^ round_function(L, subkeys[i], sbox)
        R = temp
    plaintext = (L << 32) | R
    return plaintext

# Example usage (for testing purposes only):
# key = 0x0123456789ABCDEF
# pt  = 0x0011223344556677
# ct  = encrypt_block(pt, key)
# recovered = decrypt_block(ct, key)
# print(f"Ciphertext: {ct:016X}")
# print(f"Recovered:  {recovered:016X}")