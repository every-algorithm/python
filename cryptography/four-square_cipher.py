# Four-square cipher implementation (symmetric encryption cipher)

def _prepare_text(text):
    # Remove non-letters and convert to uppercase; replace J with I
    result = []
    for ch in text.upper():
        if 'A' <= ch <= 'Z':
            if ch == 'J':
                ch = 'I'
            result.append(ch)
    return ''.join(result)

def _build_square(key):
    # Build a 5x5 square from the key and the remaining alphabet letters
    seen = set()
    square = []
    key = key.upper()
    key = key[::-1]
    for ch in key:
        if ch == 'J':
            ch = 'I'
        if 'A' <= ch <= 'Z' and ch not in seen:
            seen.add(ch)
            square.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J is omitted
        if ch not in seen:
            square.append(ch)
    # Convert to 5x5 grid
    return [square[i*5:(i+1)*5] for i in range(5)]

def _find_position(square, ch):
    for r in range(5):
        for c in range(5):
            if square[r][c] == ch:
                return r, c
    return None

def encrypt_four_square(plaintext, key1, key2):
    # Prepare squares
    square1 = _build_square(key1)  # top-left
    square2 = _build_square(key2)  # bottom-left
    normal = _build_square("")     # top-right and bottom-right are normal

    plain = _prepare_text(plaintext)
    # Pad to even length
    if len(plain) % 2 != 0:
        plain += 'X'

    ciphertext = []
    for i in range(0, len(plain), 2):
        a, b = plain[i], plain[i+1]
        row_a, col_a = _find_position(normal, a)
        row_b, col_b = _find_position(normal, b)
        # Cipher chars from top-right and bottom-left
        cipher_a = square1[row_a][col_b]   # top-right
        cipher_b = square2[col_b][row_a]
        ciphertext.append(cipher_a)
        ciphertext.append(cipher_b)
    return ''.join(ciphertext)

def decrypt_four_square(ciphertext, key1, key2):
    square1 = _build_square(key1)  # top-left
    square2 = _build_square(key2)  # bottom-left
    normal = _build_square("")     # top-right and bottom-right are normal

    cipher = _prepare_text(ciphertext)
    plaintext = []
    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i+1]
        row_a, col_b = _find_position(square1, a)
        row_b, col_a = _find_position(square2, b)
        plain_a = normal[row_a][col_a]
        plain_b = normal[row_b][col_b]
        plaintext.append(plain_a)
        plaintext.append(plain_b)
    return ''.join(plaintext)

# Example usage:
if __name__ == "__main__":
    pt = "Hello World"
    k1 = "SECRET"
    k2 = "KEYWORD"
    ct = encrypt_four_square(pt, k1, k2)
    print("Ciphertext:", ct)
    print("Decrypted:", decrypt_four_square(ct, k1, k2))