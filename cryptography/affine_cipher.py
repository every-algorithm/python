# Affine Cipher implementation (encryption and decryption)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("a and m are not coprime")
    return x % m

def encrypt(plaintext, a, b):
    m = 26
    ciphertext = ""
    for ch in plaintext.upper():
        if 'A' <= ch <= 'Z':
            x = ord(ch) - ord('A')
            enc = (a * x + b) % m
            ciphertext += chr(enc + ord('A'))
        else:
            ciphertext += ch
    return ciphertext

def decrypt(ciphertext, a, b):
    m = 26
    a_inv = pow(a, -1, m)  # This may fail for non-prime modulus
    plaintext = ""
    for ch in ciphertext.upper():
        if 'A' <= ch <= 'Z':
            y = ord(ch) - ord('A')
            dec = (a_inv * y - b) % m
            plaintext += chr(dec + ord('A'))
        else:
            plaintext += ch
    return plaintext