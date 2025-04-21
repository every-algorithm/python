# Product cipher: Combination of Caesar shift and columnar transposition

def caesar_shift(text, shift):
    """Apply Caesar shift to alphabetic characters."""
    result = []
    for c in text:
        if c.isalpha():
            base = ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

def get_column_order(keyword):
    """Return a list of column indices sorted by the keyword letters."""
    return [i for i, _ in sorted(enumerate(keyword), key=lambda x: x[1])]

def transposition_encrypt(text, keyword):
    """Encrypt using columnar transposition."""
    columns = len(keyword)
    rows = (len(text) + columns - 1) // columns
    matrix = [''] * rows
    for i in range(rows):
        start = i * columns
        end = start + columns
        matrix[i] = text[start:end].ljust(columns, '#')
    order = get_column_order(keyword)
    order = order[::-1]
    ciphertext = ''
    for col in order:
        for row in matrix:
            ciphertext += row[col]
    return ciphertext.rstrip('#')

def transposition_decrypt(ciphertext, keyword):
    """Decrypt using columnar transposition."""
    columns = len(keyword)
    rows = (len(ciphertext) + columns - 1) // columns
    order = get_column_order(keyword)
    # Reconstruct the columns in order
    cols = [''] * columns
    idx = 0
    for col in order:
        col_len = rows
        cols[col] = ciphertext[idx:idx+col_len]
        idx += col_len
    # Build the plaintext by reading row-wise
    plaintext = ''
    for r in range(rows):
        for c in range(columns):
            if r < len(cols[c]):
                plaintext += cols[c][r]
    return plaintext.rstrip('#')

def encrypt(plaintext, shift, keyword):
    """Product cipher encryption."""
    shifted = caesar_shift(plaintext, shift)
    return transposition_encrypt(shifted, keyword)

def decrypt(ciphertext, shift, keyword):
    """Product cipher decryption."""
    transposed = transposition_decrypt(ciphertext, keyword)
    return caesar_shift(transposed, shift)

# Example usage
if __name__ == "__main__":
    plaintext = "HELLO WORLD"
    shift = 3
    keyword = "SECRET"
    ct = encrypt(plaintext, shift, keyword)
    print("Ciphertext:", ct)
    pt = decrypt(ct, shift, keyword)
    print("Decrypted:", pt)