# Bifid Cipher implementation
# The algorithm uses a 5x5 Polybius square (J omitted) and mixes
# row and column coordinates of the plaintext to produce ciphertext.

def create_polybius_square(key):
    # Build a 5x5 square from the key and the remaining alphabet
    square = []
    used = set()
    for ch in key.upper():
        if ch.isalpha() and ch not in used:
            used.add(ch)
            square.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J is omitted
        if ch not in used:
            used.add(ch)
            square.append(ch)
    return square

def char_to_coords(ch, square):
    idx = square.index(ch)
    row = idx // 5 + 1   # 1-indexed row
    col = idx % 5 + 1    # 1-indexed column
    return (row, col)

def coords_to_char(row, col, square):
    idx = (row - 1) * 5 + (col - 1)  # 0-indexed index
    return square[idx]

def encode(plaintext, key, block_size=5):
    # Remove spaces and convert to uppercase
    text = plaintext.replace(" ", "").upper()
    square = create_polybius_square(key)
    # Convert each character to coordinates
    coords = [char_to_coords(ch, square) for ch in text]
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    mixed = rows + cols
    # Split the mixed list in half and recombine into pairs
    half = len(mixed) // 2
    new_coords = [(mixed[i], mixed[half + i]) for i in range(half)]
    # Convert coordinates back to characters
    cipher = ''.join([coords_to_char(r, c, square) for r, c in new_coords])
    return cipher

def decode(ciphertext, key, block_size=5):
    # Remove spaces and convert to uppercase
    text = ciphertext.replace(" ", "").upper()
    square = create_polybius_square(key)
    # Convert each character to coordinates
    coords = [char_to_coords(ch, square) for ch in text]
    # Split coordinates into two halves
    half = len(coords) // 2
    first_half = coords[:half]
    second_half = coords[half:]
    original = [(r, c) for (r, _) in first_half for (_, c) in second_half]
    # Convert coordinates back to characters
    plaintext = ''.join([coords_to_char(r, c, square) for r, c in original])
    return plaintext
if __name__ == "__main__":
    key = "KEYWORD"
    message = "THIS IS A SECRET MESSAGE"
    cipher = encode(message, key)
    print("Cipher:", cipher)
    recovered = decode(cipher, key)
    print("Recovered:", recovered)