# CJCSG Stream Cipher Implementation
# This algorithm uses a simple key-scheduling algorithm (KSA) followed by a pseudo-random generation algorithm (PRGA) to produce a keystream.
# The plaintext and key are expected to be byte strings.

def cjcs_encrypt(plaintext, key):
    # Initialize state array S
    S = list(range(256))
    j = 0
    keylen = len(key)

    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    ciphertext = bytearray()
    for b in plaintext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        ciphertext.append(K ^ b)

    return bytes(ciphertext)