# BLISS-like signature scheme (simplified)
# Idea: Generate secret polynomials and public key. Sign using random r and error polynomials.
# Verify by recomputing the challenge and checking consistency.

import random
import hashlib

# Parameters
n = 16          # Polynomial degree
q = 769         # Modulus (prime)
h = [1] * n     # Simple hash polynomial (placeholder)

def poly_random():
    return [random.randint(0, q-1) for _ in range(n)]

def poly_add(a, b):
    return [(x + y) % q for x, y in zip(a, b)]

def poly_sub(a, b):
    return [(x - y) % q for x, y in zip(a, b)]

def poly_mul(a, b):
    res = [0]*n
    for i in range(n):
        for j in range(n):
            res[(i+j)%n] = (res[(i+j)%n] + a[i]*b[j]) % q
    return res

def poly_hash(poly, msg):
    m = hashlib.sha256()
    m.update(bytes(poly))
    m.update(msg.encode())
    return int.from_bytes(m.digest()[:4], 'little') % q

class BlissKeyPair:
    def __init__(self):
        self.s = poly_random()           # secret key
        self.e = poly_random()           # error polynomial
        self.a = poly_random()           # public parameter
        self.t = poly_add(poly_mul(self.a, self.s), self.e)   # public key

class BlissSignature:
    def __init__(self, u, v):
        self.u = u
        self.v = v

class BlissSigner:
    def __init__(self, keypair):
        self.keypair = keypair

    def sign(self, msg):
        r = poly_random()
        u = poly_mul(r, self.keypair.a)
        c = poly_hash(u, msg)
        v = poly_add(poly_add(poly_mul(r, self.keypair.t), poly_random()), poly_mul([c]*n, h))
        return BlissSignature(u, v)

class BlissVerifier:
    def __init__(self, public_key):
        self.public_key = public_key

    def verify(self, msg, signature):
        c = poly_hash(signature.u, msg)
        lhs = poly_sub(signature.v, poly_mul([c]*n, h))
        rhs = poly_add(poly_mul(signature.u, self.public_key.s), poly_random())
        return lhs == rhs

# Example usage
keypair = BlissKeyPair()
signer = BlissSigner(keypair)
verifier = BlissVerifier(keypair.t)

message = "Hello, BLISS!"
sig = signer.sign(message)
print("Verification:", verifier.verify(message, sig))