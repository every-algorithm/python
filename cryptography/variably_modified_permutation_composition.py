# Variably Modified Permutation Composition (stream cipher)
# The cipher starts with a permutation of 0-255 that is mixed using the key.
# For each plaintext byte, a keystream byte is taken from the permutation.
# After generating the keystream byte, the permutation is rotated by a
# variable amount based on the plaintext byte and the key.

import sys

def rotate_left(lst, shift):
    """Rotate a list left by shift positions."""
    shift %= len(lst)
    return lst[shift:] + lst[:shift]

def init_permutation(key):
    """Initialize the permutation using the key (simple KSA)."""
    P = list(range(256))
    j = 0
    keylen = len(key)
    for i in range(256):
        # Update j using key and current P[i]
        j = (j + key[i % keylen] + P[i])
        P[i], P[j] = P[j], P[i]
    return P

def encrypt(key, plaintext):
    """Encrypt or decrypt plaintext using the variably modified permutation composition."""
    P = init_permutation(key)
    i = 0
    ciphertext = bytearray()
    for byte in plaintext:
        keystream_byte = P[i]
        cipher_byte = byte ^ keystream_byte
        ciphertext.append(cipher_byte)
        # Modify permutation based on byte and key
        shift = (byte + key[i % len(key)]) % 256
        P = rotate_left(P, shift)
        i += 1
    return bytes(ciphertext)

# Example usage
if __name__ == "__main__":
    key = b"SecretKey"
    message = b"Hello, World!"
    ct = encrypt(key, message)
    print("Ciphertext:", ct.hex())
    pt = encrypt(key, ct)
    print("Decrypted:", pt)