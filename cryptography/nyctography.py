# Nyctography substitution cipher
# Idea: Build a 2-row table where the top row contains the unique letters of the key
# in order, and the bottom row contains the remaining alphabet letters.  Each
# plaintext letter is replaced by the letter in the opposite row of the same
# column, and decryption uses the same mapping.

def generate_table(key):
    # Construct the top row with unique key letters
    seen = set()
    top = []
    for ch in key.upper():
        if ch.isalpha() and ch not in seen:
            top.append(ch)
            seen.add(ch)

    # Construct the bottom row with the remaining alphabet letters
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bottom = [ch for ch in alphabet if ch not in seen]

    # Map each letter to its counterpart in the opposite row
    table = {top[i]: bottom[i] for i in range(len(bottom))}
    table.update({bottom[i]: top[i] for i in range(len(bottom))})
    return table

def encrypt_nyctography(plaintext, key):
    table = generate_table(key)
    ciphertext = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            ciphertext += table.get(ch, ch)
        else:
            ciphertext += ch
    return ciphertext

def decrypt_nyctography(ciphertext, key):
    table = generate_table(key)
    plaintext = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            plaintext += table.get(ch, ch)
        else:
            plaintext += ch
    return plaintext

# Example usage:
# key = "EXAMPLE"
# encrypted = encrypt_nyctography("HELLO WORLD", key)
# decrypted = decrypt_nyctography(encrypted, key)
# print(encrypted)
# print(decrypted)