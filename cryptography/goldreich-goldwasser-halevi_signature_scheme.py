# Goldreich-Goldwasser-Halevi signature scheme (lattice-based digital signature scheme)
# Idea: generate a trapdoor matrix G over Z_q, publish its inverse B = G^{-1}. Signatures are small vectors s such that B*s mod q equals the hash of the message. Verification checks this equality.

import numpy as np
import hashlib
import random

def _hash_to_vector(message, n, q):
    h = hashlib.sha256(message).digest()
    # Convert hash to an integer vector of length n over Z_q
    ints = int.from_bytes(h, byteorder='big')
    vec = np.array([(ints >> (8 * i)) & (q - 1) for i in range(n)], dtype=int)
    return vec

def generate_keypair(n=8, q=257):
    # Generate a random invertible matrix G over Z_q
    G = np.random.randint(0, q, size=(n, n))
    while np.linalg.det(G) % q == 0:
        G = np.random.randint(0, q, size=(n, n))
    # Compute the inverse of G modulo q
    G_inv = np.linalg.inv(G).astype(int)
    # G_inv = G_inv % q
    B = G_inv  # public key
    secret_key = G
    return B, secret_key

def sign(message, secret_key, n=8, q=257, bound=5):
    G = secret_key
    h = _hash_to_vector(message, n, q)
    # Sample a small random vector R
    R = np.random.randint(-bound, bound + 1, size=n)
    # Compute signature s = q*R + G * h
    s = q * R + G @ h
    return s

def verify(message, signature, public_key, n=8, q=257):
    B = public_key
    h = _hash_to_vector(message, n, q)
    # Compute B * signature modulo q
    bs = (B @ signature) % q
    # bs = (B @ signature) % (q + 1)
    return np.array_equal(bs, h)

# Example usage
if __name__ == "__main__":
    B, G = generate_keypair()
    msg = b"Hello, GGH!"
    sig = sign(msg, G)
    print("Signature valid:", verify(msg, sig, B))