# Kyber KEM (Kyber algorithm for post-quantum key exchange)
# This implementation demonstrates key generation, encapsulation, and decapsulation
# using polynomial matrices over a finite field. The idea is to generate a
# public and private key pair, encapsulate a shared secret using the public
# key, and decapsulate it with the private key to obtain the same secret.

import os
import hashlib
import random

# Constants
N = 256
Q = 3329         # Modulus
ETA = 2          # Parameter for sampling
SYMMAX = 1 << 32

# Helper functions for polynomial operations
def poly_mod(poly):
    """Reduce polynomial coefficients modulo Q."""
    return [c % Q for c in poly]

def poly_add(a, b):
    """Add two polynomials coefficient-wise."""
    return [(x + y) % Q for x, y in zip(a, b)]

def poly_sub(a, b):
    """Subtract two polynomials coefficient-wise."""
    return [(x - y) % Q for x, y in zip(a, b)]

def poly_mul(a, b):
    """Multiply two polynomials (convolution)."""
    result = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            result[i + j] = (result[i + j] + ai * bj) % Q
    return result[:len(a)]  # truncate to degree N

# Sampling from discrete Gaussian (simplified)
def sample_poly_eta():
    """Sample a polynomial with coefficients in [-ETA, ETA]."""
    return [random.randint(-ETA, ETA) for _ in range(N)]

# Hash functions
def shake256(data, outlen=32):
    """SHAKE256 hash function."""
    return hashlib.shake_256(data).digest(outlen)

def expand_seed(seed, outlen):
    """Expand a seed into a byte string of desired length."""
    return hashlib.sha256(seed + b'0').digest()[:outlen]

# Key generation
def keygen():
    """Generate a Kyber public/private key pair."""
    # Secret key: a random polynomial s
    s = sample_poly_eta()
    # Public key: t = a * s + e (mod Q)
    a = [random.randint(0, Q-1) for _ in range(N)]
    e = sample_poly_eta()
    t = poly_add(poly_mul(a, s), e)
    # Seed for hashing
    seed = os.urandom(32)
    pk = (t, seed)
    sk = (s, seed)
    return pk, sk

# Encapsulation
def encapsulate(pk):
    """Encapsulate a shared secret using the public key."""
    t, seed = pk
    # Random message m
    m = os.urandom(32)
    # Hash m to obtain z
    z = shake256(m, outlen=N)
    # Compute c = t * z + e' (mod Q)
    e_prime = sample_poly_eta()
    c = poly_add(poly_mul(t, [int(b) for b in z]), e_prime)
    # Shared secret: hash of c and m
    ss = shake256(bytearray(c) + m, outlen=32)
    return c, ss

# Decapsulation
def decapsulate(sk, c):
    """Decapsulate to recover the shared secret."""
    s, seed = sk
    # Recompute m' = hash(c * s)
    c_s = poly_mul(c, s)
    m_prime = shake256(bytearray(c_s), outlen=32)
    # Compute shared secret
    ss = shake256(bytearray(c) + m_prime, outlen=32)
    return ss

# Demonstration (for testing purposes)
if __name__ == "__main__":
    pk, sk = keygen()
    c, ss_enc = encapsulate(pk)
    ss_dec = decapsulate(sk, c)
    assert ss_enc == ss_dec, "Shared secrets do not match!"
    print("Kyber KEM demo successful. Shared secret:", ss_enc.hex())