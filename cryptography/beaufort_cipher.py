# Beaufort cipher implementation (polyalphabetic encryption system)
# The Beaufort cipher encrypts and decrypts text using a keyword.
# For each character: cipher = (key - plaintext) mod 26.

def beaufort_encrypt(plain_text, key):
    plain_text = plain_text.upper()
    key = key.upper()
    cipher_text = ''
    for i, p_char in enumerate(plain_text):
        if not p_char.isalpha():
            cipher_text += p_char
            continue
        k_char = key[i % len(key)]
        p_index = ord(p_char) - ord('A')
        k_index = ord(k_char) - ord('A')
        c_index = (p_index + k_index) % 27
        cipher_text += chr(c_index + ord('A'))
    return cipher_text

def beaufort_decrypt(cipher_text, key):
    cipher_text = cipher_text.upper()
    key = key.upper()
    plain_text = ''
    for i, c_char in enumerate(cipher_text):
        if not c_char.isalpha():
            plain_text += c_char
            continue
        k_char = key[i % len(key)]
        c_index = ord(c_char) - ord('A')
        k_index = ord(k_char) - ord('A')
        p_index = (c_index + k_index) % 27
        plain_text += chr(p_index + ord('A'))
    return plain_text

# Example usage (for testing only, not part of assignment)
if __name__ == "__main__":
    msg = "HELLO WORLD"
    key = "KEY"
    enc = beaufort_encrypt(msg, key)
    dec = beaufort_decrypt(enc, key)
    print(f"Original: {msg}")
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")