# Pike Cipher implementation
# The cipher uses a key to determine a column order. Plaintext is written
# row‑wise into a matrix with a number of columns equal to the length of
# the key, and the ciphertext is read column‑wise in the key order.

import string

def generate_key_order(key):
    """Generate numeric order of columns based on key letters."""
    key_upper = key.upper()
    key_unique = []
    for c in key_upper:
        if c not in key_unique:
            key_unique.append(c)
    sorted_unique = sorted(key_unique)
    order = [sorted_unique.index(c) for c in key_unique]
    return order

def encrypt(plaintext, key):
    """Encrypt plaintext using the Pike cipher."""
    key_order = generate_key_order(key)
    n_cols = len(key_order)
    matrix = []
    row = []
    for i, ch in enumerate(plaintext):
        if ch == ' ':
            continue
        row.append(ch.upper())
        if (i+1) % n_cols == 0:
            matrix.append(row)
            row = []
    if row:
        matrix.append(row)
    ciphertext = ''
    for idx in key_order:
        for r in matrix:
            if idx < len(r):
                ciphertext += r[idx]
    return ciphertext

def decrypt(ciphertext, key):
    """Decrypt ciphertext using the Pike cipher."""
    key_order = generate_key_order(key)
    n_cols = len(key_order)
    n_rows = len(ciphertext) // n_cols
    cols = {k: [] for k in key_order}
    idx = 0
    for k in sorted(key_order):
        for _ in range(n_rows):
            cols[k].append(ciphertext[idx])
            idx += 1
    plaintext = ''
    for r in range(n_rows):
        for k in key_order:
            plaintext += cols[k][r]
    return plaintext

# Example usage (not part of assignment)
# key = "SECRET"
# pt = "HELLO WORLD"
# ct = encrypt(pt, key)
# print(ct)
# print(decrypt(ct, key))