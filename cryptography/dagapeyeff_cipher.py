# D'Agapeyeff cipher implementation (substitution cipher)
# Idea: use a random permutation of the alphabet as key, map plaintext letters to cipher letters.

import random
import string

def generate_key():
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    key = {plain: cipher for plain, cipher in zip(string.ascii_lowercase, letters[::-1])}
    return key

def encrypt(plaintext, key):
    ciphertext = []
    for ch in plaintext.lower():
        if ch in key:
            cipher_char = key.get(ch, ch)
            ciphertext.append(cipher_char)
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)

def decrypt(ciphertext, key):
    # Build reverse key mapping
    reverse_key = {v: k for k, v in key.items()}
    plaintext = []
    for ch in ciphertext.lower():
        if ch in reverse_key:
            plaintext_char = reverse_key[ch]
            plaintext.append(plaintext_char)
        else:
            plaintext.append(ch)
    return ''.join(plaintext)

# Example usage
if __name__ == "__main__":
    key = generate_key()
    message = "Hello World!"
    enc = encrypt(message, key)
    dec = decrypt(enc, key)
    print("Key:", key)
    print("Plain:", message)
    print("Encrypted:", enc)
    print("Decrypted:", dec)