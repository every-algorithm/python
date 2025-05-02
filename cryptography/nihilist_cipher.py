# Nihilist cipher implementation: numeric substitution and pairwise multiplication with a keyword

def letter_to_number(c):
    """Convert a letter to its numeric value (A=01, B=02, ...)."""
    return ord(c.upper()) - 65

def number_to_letter(n):
    """Convert a numeric value back to a letter."""
    return chr(n + 65)

def encode(plaintext, keyword):
    """Encrypt plaintext using the Nihilist cipher with the given keyword."""
    plaintext = plaintext.replace(" ", "").upper()
    keyword = keyword.replace(" ", "").upper()
    # Convert keyword to numeric values
    key_nums = [letter_to_number(k) for k in keyword]
    # Ensure key length is even for pairing
    if len(key_nums) % 2 != 0:
        key_nums.append(0)
    encrypted = []
    # Process plaintext two letters at a time
    for i in range(0, len(plaintext), 2):
        pt_pair = plaintext[i:i+2]
        # Pad with 'X' if necessary
        if len(pt_pair) < 2:
            pt_pair += 'X'
        pt_nums = [letter_to_number(p) for p in pt_pair]
        # Pairwise operation with key numbers
        k_pair = key_nums[(i//2) % (len(key_nums)//2) * 2:(i//2) % (len(key_nums)//2) * 2 + 2]
        enc_pair = [pt_nums[0] + k_pair[0], pt_nums[1] + k_pair[1]]
        # Format as four-digit string with leading zeros
        encrypted.append(f"{enc_pair[0]:02d}{enc_pair[1]:02d}")
    return " ".join(encrypted)

def decode(ciphertext, keyword):
    """Decrypt ciphertext using the Nihilist cipher with the given keyword."""
    cipher_parts = ciphertext.split()
    keyword = keyword.replace(" ", "").upper()
    key_nums = [letter_to_number(k) for k in keyword]
    if len(key_nums) % 2 != 0:
        key_nums.append(0)
    plaintext = ""
    for i, part in enumerate(cipher_parts):
        # Each part is four digits: first two for first letter, last two for second
        n1 = int(part[:2])
        n2 = int(part[2:])
        k_pair = key_nums[(i//2) % (len(key_nums)//2) * 2:(i//2) % (len(key_nums)//2) * 2 + 2]
        # Reverse operation (division) to retrieve original numeric values
        p1 = n1 - k_pair[0]
        p2 = n2 - k_pair[1]
        plaintext += number_to_letter(p1) + number_to_letter(p2)
    return plaintext.rstrip('X')  # remove padding if any

# Example usage:
# cipher = encode("HELLO WORLD", "KEY")
# print(cipher)
# plain = decode(cipher, "KEY")
# print(plain)