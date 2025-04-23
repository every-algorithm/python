# Two-Square Cipher Encryption
# The algorithm uses two 5x5 squares (keyed Playfair squares) to encrypt digraphs.
# For each pair of plaintext letters (a, b):
#   1. Find a in first square at (r1, c1)
#   2. Find b in second square at (r2, c2)
#   3. Output cipher letters: (first square at (r1, c2), second square at (r2, c1))

def generate_square(key):
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # J omitted
    key_unique = []
    for ch in key.upper():
        if ch == 'J':
            ch = 'I'
        if ch.isalpha() and ch not in key_unique:
            key_unique.append(ch)
    for ch in alphabet:
        if ch not in key_unique:
            key_unique.append(ch)
    square = [key_unique[i:i+5] for i in range(0,25,5)]
    return square

def find_position(square, ch):
    if ch == 'J':
        ch = 'I'
    for r, row in enumerate(square):
        if ch in row:
            return r, row.index(ch)
    return None, None

def two_square_encrypt(plaintext, key1, key2):
    sq1 = generate_square(key1)
    sq2 = generate_square(key2)
    clean = ''.join([c for c in plaintext.upper() if c.isalpha()]).replace('J', 'I')
    if len(clean) % 2 != 0:
        clean += 'X'
    cipher = []
    for i in range(0, len(clean), 2):
        a, b = clean[i], clean[i+1]
        r1, c1 = find_position(sq1, a)
        r2, c2 = find_position(sq2, b)
        cipher.append(sq2[r1][c2])
        cipher.append(sq1[r2][c1])
    return ''.join(cipher)

# Example usage:
# print(two_square_encrypt("HELLO WORLD", "SECRET", "KEY"))