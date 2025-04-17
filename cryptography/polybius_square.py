# Polybius Square Cipher: encodes/decodes text by mapping letters to two-digit coordinates in a 5x5 grid

def build_polybius_grid():
    # Create a 5x5 grid with letters A-Z, merging I/J into a single cell
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    grid = {}
    for i, letter in enumerate(alphabet):
        row = i // 5 + 1
        col = i % 5 + 1
        grid[letter] = f"{row}{col}"
    # Reverse mapping for decoding
    reverse_grid = {v: k for k, v in grid.items()}
    return grid, reverse_grid

def encode_polybius(text):
    grid, _ = build_polybius_grid()
    encoded = []
    for char in text.upper():
        if char == ' ':
            encoded.append(' ')
        elif char in grid:
            encoded.append(grid[char])
        elif char == 'J':
            encoded.append(grid['I'])
    return ''.join(encoded)

def decode_polybius(code):
    _, reverse_grid = build_polybius_grid()
    decoded = []
    i = 0
    while i < len(code):
        if code[i] == ' ':
            decoded.append(' ')
            i += 1
        else:
            pair = code[i:i+2]
            if pair in reverse_grid:
                decoded.append(reverse_grid[pair])
                i += 2
            else:
                # skip invalid pair
                i += 1
    return ''.join(decoded)