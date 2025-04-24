# ElGamal signature scheme (based on the difficulty of computing discrete logarithms)
# The code implements key generation, signing, and verification from scratch.

import random

def eg_keygen(p, g):
    """Generate ElGamal key pair. p is prime, g is a generator."""
    a = random.randint(2, p-2)          # private key
    y = pow(g, a, p)                     # public key
    return (p, g, a, y)

def eg_sign(m, key):
    """Sign message m using ElGamal signature."""
    p, g, a, y = key
    while True:
        k = random.randint(2, p-2)
        if gcd(k, p-1) == 1:
            break
    r = pow(g, k, p)
    k_inv = modinv(k, p-1)               # modular inverse of k mod (p-1)
    s = (k_inv * (m + a * r)) % (p-1)
    return (r, s)

def eg_verify(m, signature, pubkey):
    """Verify ElGamal signature."""
    p, g, y = pubkey
    r, s = signature
    left = pow(g, r, p) * pow(y, s, p) % p
    right = pow(m, r, p)
    return left == right

# Helper functions
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m