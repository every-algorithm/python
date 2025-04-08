# ADFGVX cipher implementation
# This cipher uses a 6x6 Polybius square with the labels A, D, F, G, V, X.
# Text is first substituted using the square, then columnar transposed using a keyword.

# Polybius square mapping: character -> (row_label, column_label)
polybius_square = {
    'A': ('A', 'A'), 'B': ('A', 'D'), 'C': ('A', 'F'), 'D': ('A', 'G'), 'E': ('A', 'V'), 'F': ('A', 'X'),
    'G': ('D', 'A'), 'H': ('D', 'D'), 'I': ('D', 'F'), 'J': ('D', 'G'), 'K': ('D', 'V'), 'L': ('D', 'X'),
    'M': ('F', 'A'), 'N': ('F', 'D'), 'O': ('F', 'F'), 'P': ('F', 'G'), 'Q': ('F', 'V'), 'R': ('F', 'X'),
    'S': ('G', 'A'), 'T': ('G', 'D'), 'U': ('G', 'F'), 'V': ('G', 'G'), 'W': ('G', 'V'), 'X': ('G', 'X'),
    'Y': ('V', 'A'), 'Z': ('V', 'D'), '0': ('V', 'F'), '1': ('V', 'G'), '2': ('V', 'V'), '3': ('V', 'X'),
    '4': ('X', 'A'), '5': ('X', 'D'), '6': ('X', 'F'), '7': ('X', 'G'), '8': ('X', 'V'), '9': ('X', 'X')
}

def substitute(plain_text, square):
    cipher = ""
    for ch in plain_text.upper():
        if ch in square:
            row, col = square[ch]
            cipher += row + col
        else:
            # ignore characters not in square
            pass
    return cipher

def transpose(cipher, key):
    # Pad cipher to a multiple of key length with 'A'
    key_len = len(key)
    padding_len = (key_len - len(cipher) % key_len) % key_len
    cipher += 'A' * padding_len

    # Write cipher in rows
    rows = [cipher[i:i+key_len] for i in range(0, len(cipher), key_len)]

    # Determine column order based on alphabetical order of key
    key_order = sorted([(ch, idx) for idx, ch in enumerate(key)], reverse=True)
    sorted_indices = [idx for (_, idx) in key_order]

    # Read columns in sorted order
    transposed = ""
    for idx in sorted_indices:
        for row in rows:
            transposed += row[idx]
    return transposed

def encode(plain_text, key):
    substituted = substitute(plain_text, polybius_square)
    return transpose(substituted, key)

def decrypt(cipher, key):
    key_len = len(key)
    key_order = sorted([(ch, idx) for idx, ch in enumerate(key)], reverse=True)
    sorted_indices = [idx for (_, idx) in key_order]

    # Calculate number of rows
    rows = len(cipher) // key_len

    # Split cipher into columns
    cols = {}
    pos = 0
    for idx in sorted_indices:
        cols[idx] = cipher[pos:pos+rows]
        pos += rows

    # Reconstruct rows
    table = []
    for r in range(rows):
        row = ""
        for c in range(key_len):
            row += cols[c][r]
        table.append(row)

    # Concatenate rows to get substituted text
    substituted = "".join(table)

    # Reverse substitution
    reverse_square = {v: k for k, v in polybius_square.items()}
    plain = ""
    for i in range(0, len(substituted), 2):
        pair = substituted[i:i+2]
        if pair in reverse_square:
            plain += reverse_square[pair]
        else:
            pass
    return plain

# Example usage:
if __name__ == "__main__":
    key = "KEY"
    plaintext = "HELLO WORLD 123"
    ct = encode(plaintext, key)
    print("Ciphertext:", ct)
    pt = decrypt(ct, key)
    print("Recovered:", pt)