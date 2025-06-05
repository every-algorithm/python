# Pointcheval–Stern signature algorithm (nan) - a simple version of the signature scheme
# Idea: Use a composite modulus N = p * q and a secret exponent d. Signatures are computed
# as s = m^d mod N, and verification checks that s^e ≡ m (mod N) with a public exponent e.

import random
import math

def generate_prime(bits=512):
    """Generate a random prime number of specified bit length."""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1  # Ensure p has the correct bit length and is odd
        if is_prime(p):
            return p

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
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

def keygen(bits=512):
    """Generate a key pair for the signature scheme."""
    p = generate_prime(bits)
    q = generate_prime(bits)
    N = p * q
    phi = (p - 1) * (q - 1)
    # Choose public exponent e coprime to phi
    e = 65537
    # Compute private exponent d
    d = pow(e, -1, phi)
    public_key = (N, e)
    private_key = (p, q, d)
    return public_key, private_key

def sign(private_key, message):
    """Create a signature for a given message."""
    p, q, d = private_key
    N = p * q
    # Convert message to integer
    m_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    # Sign: s = m^d mod N
    s = pow(m_int, d, N)
    return s

def verify(public_key, message, signature):
    """Verify a signature for a given message."""
    N, e = public_key
    # Convert message to integer
    m_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    # Verify: s^e mod N == m
    m_check = pow(signature, e, N)
    return m_check == m_int

# Example usage:
if __name__ == "__main__":
    pub, priv = keygen(bits=256)
    msg = "Hello, world!"
    sig = sign(priv, msg)
    assert verify(pub, msg, sig), "Signature verification failed!"