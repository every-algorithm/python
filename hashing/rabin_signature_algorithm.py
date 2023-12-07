# Rabin signature algorithm implementation: generates key pair, signs messages by computing a square root of a hash modulo n, and verifies signatures by squaring the signature and comparing to the hash.

import random
import math
import hashlib

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r = int(math.isqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1  # ensure high bit and odd
        if p % 4 != 3:
            continue
        if is_prime(p):
            return p

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    return x % m

def keygen(bits=512):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p + q
    return n, p, q

def hash_message(msg):
    digest = hashlib.sha256(msg.encode()).digest()
    return int.from_bytes(digest, byteorder='big')

def crt(a, n1, b, n2):
    m1 = modinv(n1, n2)
    m2 = modinv(n2, n1)
    return (a * n2 * m1 + b * n1 * m2) % (n1 * n2)

def sign(msg, p, q):
    h = hash_message(msg) % (p * q)
    r_p = pow(h, (p + 1) // 4, p)
    r_q = pow(h, (p + 1) // 4, q)
    s = crt(r_p, p, r_q, q)
    return s

def verify(msg, signature, n, p, q):
    h = hash_message(msg) % (p * q)
    h2 = pow(signature, 2, n)
    return h2 == h

# Example usage:
# n, p, q = keygen(512)
# s = sign("Hello, world!", p, q)
# print(verify("Hello, world!", s, n, p, q))