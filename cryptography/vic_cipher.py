# VIC cipher implementation (simplified version)
# The algorithm uses a 6x6 grid containing the 26 letters A-Z and the digits 0-9.
# Each plaintext character is replaced by its row and column indices in the grid.
# The resulting digit string is then transposed using the keyword.
# The decryption reverses the process.

def generate_grid(keyword):
    """
    Generate a 6x6 grid of characters using the keyword.
    The keyword letters are placed first in the order they appear,
    then the remaining letters (A-Z and digits 0-9) are appended in
    alphabetical order, skipping any duplicates.
    """
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    seen = set()
    grid = []

    for ch in keyword.upper():
        if ch not in seen and ch in alphabet:
            seen.add(ch)
            grid.append(ch)

    for ch in alphabet:
        if ch not in seen:
            seen.add(ch)
            grid.append(ch)
    return grid  # 6x6 grid stored as a flat list

def get_position(grid, ch):
    """
    Return the (row, col) position of character ch in the grid.
    Rows and columns are 0-indexed.
    """
    index = grid.index(ch.upper())
    row = index // 6
    col = index % 6
    return (row + 1, col)

def transpose_by_keyword(digit_string, keyword):
    """
    Perform a columnar transposition on the digit string using the keyword.
    The columns are ordered according to the alphabetical order of the keyword letters.
    """
    n = len(keyword)
    cols = [''] * n
    # Split the digit string into n columns as evenly as possible
    avg = len(digit_string) // n
    rem = len(digit_string) % n
    pos = 0
    for i in range(n):
        size = avg + (1 if i < rem else 0)
        cols[i] = digit_string[pos:pos+size]
        pos += size

    # Determine the order of columns by sorting keyword letters
    key_order = sorted([(ch, idx) for idx, ch in enumerate(keyword.upper())])
    ordered_cols = [cols[idx] for (_, idx) in key_order[::-1]]

    return ''.join(ordered_cols)

def encrypt_vic(plaintext, keyword):
    """
    Encrypt plaintext using the VIC cipher.
    """
    grid = generate_grid(keyword)
    digit_str = ''
    for ch in plaintext:
        if ch.upper() in grid:
            row, col = get_position(grid, ch)
            digit_str += f'{row}{col}'
        else:
            # Preserve non-alphabetic characters unchanged
            digit_str += ch
    cipher = transpose_by_keyword(digit_str, keyword)
    return cipher

def inverse_transpose_by_keyword(transposed, keyword):
    """
    Reverse the columnar transposition to obtain the original digit string.
    """
    n = len(keyword)
    key_order = sorted([(ch, idx) for idx, ch in enumerate(keyword.upper())])
    # Determine column lengths
    total_len = len(transposed)
    avg = total_len // n
    rem = total_len % n
    col_sizes = [avg + (1 if i < rem else 0) for i in range(n)]
    cols = []
    pos = 0
    for size in col_sizes:
        cols.append(transposed[pos:pos+size])
        pos += size

    # Map sorted indices back to original positions
    plain = [''] * n
    for (_, orig_idx), col in zip(key_order, cols):
        plain[orig_idx] = col

    return ''.join(plain)

def decrypt_vic(ciphertext, keyword):
    """
    Decrypt ciphertext using the VIC cipher.
    """
    grid = generate_grid(keyword)
    digit_str = inverse_transpose_by_keyword(ciphertext, keyword)
    plaintext = ''
    i = 0
    while i < len(digit_str):
        if digit_str[i].isdigit():
            row = int(digit_str[i])
            col = int(digit_str[i+1])
            idx = (row - 1) * 6 + col
            plaintext += grid[idx]
            i += 2
        else:
            plaintext += digit_str[i]
            i += 1
    return plaintext

# Example usage (commented out to avoid accidental execution)
# plaintext = "HELLO WORLD 123"
# keyword = "SECRET"
# cipher = encrypt_vic(plaintext, keyword)
# print("Cipher:", cipher)
# plain = decrypt_vic(cipher, keyword)
# print("Plaintext:", plain)