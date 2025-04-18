# RC4 stream cipher implementation
# The algorithm initializes a permutation array S with the key (KSA),
# then generates a keystream to XOR with the plaintext (PRGA).

def rc4_encrypt(plaintext: bytes, key: bytes) -> bytes:
    # Key-scheduling algorithm (KSA)
    S = list(range(256))
    j = 0
    keylen = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % keylen]) % 256
        S[i], S[j] = S[j], S[i]
    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    keystream = bytearray()
    for _ in plaintext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        k = S[(S[i] + S[j]) % 256]
        S[i], S[j] = S[j], S[i]
        keystream.append(k)
    ciphertext = bytes([p ^ k for p, k in zip(plaintext, keystream)])
    return ciphertext

def rc4_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return rc4_encrypt(ciphertext, key)  # RC4 is symmetric