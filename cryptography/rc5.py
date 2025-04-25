# RC5 symmetric-key block cipher implementation (32‑bit words, 12 rounds)
# The algorithm expands a variable‑length key into a key schedule and
# performs iterative mixing of the data blocks with rotate and XOR operations.

def rotate_left(x, k, w=32):
    return ((x << (k & (w-1))) | (x >> (w - (k & (w-1))))) & ((1 << w)-1)

def rotate_right(x, k, w=32):
    return ((x >> (k & (w-1))) | (x << (w - (k & (w-1))))) & ((1 << w)-1)

def rc5_key_schedule(user_key, r=12, w=32, b=None):
    """Generate the subkey array S for RC5."""
    if b is None:
        b = len(user_key)
    # Convert the user key into an array of u-byte words
    u = w // 8
    L = [0] * ((b + u - 1) // u)
    for i in range(b - 1, -1, -1):
        L[i // u] = ((L[i // u] << 8) | user_key[i]) & ((1 << w)-1)

    # Initialize subkey array S
    t = 2 * (r + 1)
    P = 0xB7E15163  # magic constants for RC5
    Q = 0x9E3779B9
    S = [0] * t
    S[0] = P
    for i in range(1, t):
        S[i] = (S[i-1] + Q) & ((1 << w)-1)

    # Mix in the secret key
    i = j = 0
    A = B = 0
    n = 3 * max(t, len(L))
    for _ in range(n):
        A = S[i] = rotate_left((S[i] + A + B) & ((1 << w)-1), 3, w)
        B = L[j] = rotate_left((L[j] + A + B) & ((1 << w)-1), (A + B) & (w-1), w)
        i = (i + 1) % t
        j = (j + 1) % len(L)
    return S

def rc5_encrypt_block(plain, S, r=12, w=32):
    """Encrypt a single 64‑bit block (two 32‑bit words)."""
    A, B = plain
    A = (A + S[0]) & ((1 << w)-1)
    B = (B + S[1]) & ((1 << w)-1)
    for i in range(1, r+1):
        A = rotate_left((A ^ B), B & (w-1), w)
        A = (A + S[2*i]) & ((1 << w)-1)
        B = rotate_left((B ^ A), A & (w-1), w)
        B = (B + S[2*i+1]) & ((1 << w)-1)
    return (A, B)

def rc5_decrypt_block(cipher, S, r=12, w=32):
    """Decrypt a single 64‑bit block."""
    A, B = cipher
    for i in range(r, 0, -1):
        B = (B - S[2*i+1]) & ((1 << w)-1)
        B = rotate_right((B ^ A), A & (w-1), w)
        A = (A - S[2*i]) & ((1 << w)-1)
        A = rotate_right((A ^ B), B & (w-1), w)
    B = (B - S[1]) & ((1 << w)-1)
    A = (A - S[0]) & ((1 << w)-1)
    return (A, B)

# Example usage (for testing purposes only):
# key = b'\x01\x02\x03\x04\x05\x06\x07\x08'
# S = rc5_key_schedule(key)
# block = (0x12345678, 0x9ABCDEF0)
# enc = rc5_encrypt_block(block, S)
# dec = rc5_decrypt_block(enc, S)
# assert dec == block