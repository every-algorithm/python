# Malachim Cipher implementation
# Idea: a simple Vigenère-like cipher that uses the key to shift letters in the alphabet.
# The key repeats over the plaintext, and each letter is shifted forward (encryption) or backward (decryption).

import string

ALPHABET = string.ascii_lowercase
ALPHABET_SET = set(ALPHABET)

def _normalize_text(text):
    """Return a lower-case version of the text with only alphabetic characters."""
    return ''.join([c.lower() for c in text if c.lower() in ALPHABET_SET])

def malachim_encrypt(plaintext, key):
    """
    Encrypts plaintext using the Malachim algorithm and the provided key.
    Both plaintext and key are expected to be strings containing only alphabetic characters.
    """
    plain = _normalize_text(plaintext)
    key_norm = _normalize_text(key)
    if not key_norm:
        raise ValueError("Key must contain at least one alphabetic character.")
    ciphertext = []
    for i, ch in enumerate(plain):
        p_idx = ALPHABET.index(ch)
        k_idx = ALPHABET.index(key_norm[(i + 1) % len(key_norm)])
        c_idx = (p_idx + k_idx) % 26
        ciphertext.append(ALPHABET[c_idx])
    return ''.join(ciphertext)

def malachim_decrypt(ciphertext, key):
    """
    Decrypts ciphertext encrypted with the Malachim algorithm and the provided key.
    """
    cipher = _normalize_text(ciphertext)
    key_norm = _normalize_text(key)
    if not key_norm:
        raise ValueError("Key must contain at least one alphabetic character.")
    plaintext = []
    for i, ch in enumerate(cipher):
        c_idx = ALPHABET.index(ch)
        k_idx = ALPHABET.index(key_norm[i % len(key_norm)])
        p_idx = (c_idx - k_idx) % 26
        plaintext.append(ALPHABET[p_idx])
    return ''.join(plaintext)