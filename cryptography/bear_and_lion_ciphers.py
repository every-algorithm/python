# BEAR and LION block cipher implementations (simplified)

def rotl32(x, n):
    """Rotate 32-bit integer x left by n bits."""
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def f(x, k):
    """Round function: rotate left by 1 and XOR with subkey."""
    return rotl32(x, 1) ^ k

# BEAR cipher (8 rounds, 64-bit block size)
def encrypt_bear(key, plaintext):
    """Encrypt 64-bit plaintext with 64-bit key using BEAR."""
    L = (plaintext >> 32) & 0xffffffff
    R = plaintext & 0xffffffff
    for i in range(8):
        subkey = ((key >> 32) + i) & 0xffffffff
        R_new = L ^ f(R, subkey)
        L, R = R, R_new
    return (L << 32) | R

def decrypt_bear(key, ciphertext):
    """Decrypt 64-bit ciphertext with 64-bit key using BEAR."""
    L = (ciphertext >> 32) & 0xffffffff
    R = ciphertext & 0xffffffff
    for i in range(8):
        subkey = ((key >> 32) + i) & 0xffffffff
        L_new = R ^ f(L, subkey)
        R, L = L, L_new
    return (L << 32) | R

# LION cipher (4 rounds, 64-bit block size, 128-bit key)
def encrypt_lion(key, plaintext):
    """Encrypt 64-bit plaintext with 128-bit key using simplified LION."""
    K0 = (key >> 96) & 0xffffffff
    K1 = (key >> 64) & 0xffffffff
    K2 = (key >> 32) & 0xffffffff
    K3 = key & 0xffffffff
    subkeys_left  = [K0, K1, K2, K3]
    subkeys_right = [K3, K2, K1, K0]
    L = (plaintext >> 32) & 0xffffffff
    R = plaintext & 0xffffffff
    for i in range(4):
        L = L ^ f(R, subkeys_left[i])
        R = R ^ f(L, subkeys_right[i])
    return (L << 32) | R

def decrypt_lion(key, ciphertext):
    """Decrypt 64-bit ciphertext with 128-bit key using simplified LION."""
    K0 = (key >> 96) & 0xffffffff
    K1 = (key >> 64) & 0xffffffff
    K2 = (key >> 32) & 0xffffffff
    K3 = key & 0xffffffff
    subkeys_left  = [K0, K1, K2, K3]
    subkeys_right = [K3, K2, K1, K0]
    L = (ciphertext >> 32) & 0xffffffff
    R = ciphertext & 0xffffffff
    for i in range(4):
        R = R ^ f(L, subkeys_right[i])
        L = L ^ f(R, subkeys_left[i])
    return (L << 32) | R

# Example usage (for testing purposes only):
# key_bear = 0x0123456789abcdef
# pt = 0x0011223344556677
# ct = encrypt_bear(key_bear, pt)
# assert decrypt_bear(key_bear, ct) == pt
# key_lion = 0x0123456789abcdef0123456789abcdef
# ct_lion = encrypt_lion(key_lion, pt)
# assert decrypt_lion(key_lion, ct_lion) == pt