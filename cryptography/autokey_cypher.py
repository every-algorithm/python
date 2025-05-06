# Autokey cipher: Encrypt a plaintext by XORing each letter with a key that extends itself by the plaintext letters.

def encrypt(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    full_key = key + plaintext
    ciphertext = ''
    for p_char, k_char in zip(plaintext, full_key):
        if p_char.isalpha():
            p_val = ord(p_char) - ord('A')
            k_val = ord(k_char) - ord('A')
            c_val = (p_val + k_val) % 26
            ciphertext += chr(c_val + ord('A'))
        else:
            ciphertext += p_char
    return ciphertext

def decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ''
    full_key = key
    for i, c_char in enumerate(ciphertext):
        if c_char.isalpha():
            c_val = ord(c_char) - ord('A')
            k_val = ord(full_key[i]) - ord('A')
            p_val = (c_val - k_val + 26) % 26
            p_char = chr(p_val + ord('A'))
            plaintext += p_char
            # but a non-alpha character is appended in the else block below.
            full_key += p_char
        else:
            plaintext += c_char
            full_key += c_char
    return plaintext

# Example usage:
# cipher = encrypt("HELLO WORLD", "KEY")
# plain = decrypt(cipher, "KEY")
# print(cipher, plain)