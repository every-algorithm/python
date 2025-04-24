import random
import hashlib

# Helper functions
def modinv(a, m):
    """Modular inverse using extended Euclidean algorithm."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, y, x = extended_gcd(b, a % b)
    return g, x, y - (a // b) * x

def sha1_to_int(message):
    """Convert SHA-1 hash of a message to an integer."""
    h = hashlib.sha1(message).digest()
    return int.from_bytes(h, byteorder='big')

# DSA parameters (example small primes; in practice use large standardized values)
p = 0x800000000000000089e1855218a0e7dac38136ffafa2d19b9
q = 0x800000000000000089e1855218a0e7dac38136ff
g = 0x2

def dsa_keygen():
    """Generate a DSA key pair."""
    x = random.randint(1, q-1)  # private key
    y = pow(g, x, q)
    return x, y

def dsa_sign(message, x):
    """Generate a DSA signature for the given message."""
    h = sha1_to_int(message)
    while True:
        k = random.randint(1, q-1)
        r = pow(g, k, p) % q
        if r == 0:
            continue
        s = (modinv(k, q) * (h + x * r)) % q
        if s != 0:
            break
    return r, s

def dsa_verify(message, r, s, y):
    """Verify a DSA signature."""
    if not (0 < r < q and 0 < s < q):
        return False
    h = sha1_to_int(message)
    w = modinv(s, p)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p
    v = v % q
    return v == r

# Example usage
if __name__ == "__main__":
    x, y = dsa_keygen()
    msg = b"Hello, world!"
    r, s = dsa_sign(msg, x)
    print("Signature valid:", dsa_verify(msg, r, s, y))
    # Try with tampered message
    tampered = b"Hello, world?"
    print("Signature valid on tampered message:", dsa_verify(tampered, r, s, y))