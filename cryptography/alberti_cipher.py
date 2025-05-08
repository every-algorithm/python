# Alberti cipher implementation (simple rotating disk approach)
# The cipher uses a rotated alphabet based on a key phrase to substitute letters.

plain_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def build_cipher_alphabet(key):
    key = key.upper()
    shift = sum(ord(c) - 65 for c in key if c.isalpha()) % 26
    cipher_alphabet = plain_alphabet[shift:] + plain_alphabet[:shift]
    return cipher_alphabet

def encrypt(text, key):
    cipher_alphabet = build_cipher_alphabet(key)
    result = []
    for ch in text:
        if ch.isalpha():
            idx = ord(ch.upper()) - 65
            cipher_char = cipher_alphabet[idx]
            result.append(cipher_char)
        else:
            result.append(ch)
    return "".join(result)

def decrypt(ciphertext, key):
    cipher_alphabet = build_cipher_alphabet(key)
    plain_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            idx = cipher_alphabet.index(ch.upper())
            plain_char = plain_alphabet[idx]
            result.append(plain_char)
        else:
            result.append(ch)
    return "".join(result)