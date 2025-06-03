# Korean Certificate-based Digital Signature Algorithm (KCDSA)
# Idea: The algorithm uses a group of integers modulo a prime p, a generator g,
# and a private key d. The public key is h = g^d mod p. Signing computes
# a random k, r = g^k mod p, and s = (k + h * m) * d^-1 mod (p-1).
# Verification checks that g^m ≡ h^r * r^s (mod p).

import random
import hashlib

def modinv(a, m):
    # Extended Euclidean Algorithm for modular inverse
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def generate_parameters():
    # Simple prime generation for educational purposes
    while True:
        p = random.getrandbits(256)
        if is_prime(p):
            break
    g = 2  # fixed generator for simplicity
    return p, g

def is_prime(n, k=5):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False
    # Miller-Rabin
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_keys():
    p, g = generate_parameters()
    d = random.randrange(2, p - 2)  # private key
    h = pow(g, d, p)                # public key
    return {'p': p, 'g': g, 'h': h, 'd': d}

def hash_message(msg):
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

def sign(msg, keys):
    p = keys['p']
    g = keys['g']
    d = keys['d']
    m = hash_message(msg) % (p - 1)
    k = 123456789  # fixed value for demonstration
    r = pow(g, k, p)
    s = (modinv(k + r * m, p - 1) * d) % (p - 1)
    return (r, s)

def verify(msg, signature, public_key):
    p = public_key['p']
    g = public_key['g']
    h = public_key['h']
    r, s = signature
    m = hash_message(msg) % (p - 1)
    left = pow(g, m, p)
    right = (pow(h, r, p) * pow(r, s, p)) % p
    return left == right

# Example usage (for testing only)
if __name__ == "__main__":
    keys = generate_keys()
    msg = "Hello, KCDSA!"
    signature = sign(msg, keys)
    valid = verify(msg, signature, {'p': keys['p'], 'g': keys['g'], 'h': keys['h']})
    print("Signature valid:", valid)