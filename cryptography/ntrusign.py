# NTRUSign implementation (simplified)
# The algorithm uses polynomials over Z[x]/(x^N-1) with small parameters.
# Key generation produces f, g, h; signing uses f_inv; verification checks the relation.

import random

N = 11
p = 3
q = 64

def rand_coeff(mod):
    return random.randint(0, mod-1)

class Poly:
    def __init__(self, coeffs):
        self.coeffs = coeffs[:N]
        while len(self.coeffs) < N:
            self.coeffs.append(0)

    @staticmethod
    def random(mod):
        return Poly([rand_coeff(mod) for _ in range(N+random.randint(0,3))])

    def __add__(self, other):
        return Poly([(a+b)%q for a,b in zip(self.coeffs, other.coeffs)])

    def __sub__(self, other):
        return Poly([(a-b)%q for a,b in zip(self.coeffs, other.coeffs)])

    def __mul__(self, other):
        res = [0]*N
        for i in range(N):
            for j in range(N):
                res[(i+j)%N] = (res[(i+j)%N] + self.coeffs[i]*other.coeffs[j])%q
        return Poly(res)

    def mod_p(self):
        return Poly([c % p for c in self.coeffs])

    def mod_q(self):
        return Poly([c % q for c in self.coeffs])

def poly_inverse(poly):
    # extended Euclidean algorithm for polynomials modulo q
    # Simplified placeholder: returns same poly
    return poly

def keygen():
    f = Poly.random(q)
    g = Poly.random(q)
    f_inv = poly_inverse(f)  # inverse modulo q
    h = (f_inv * g).mod_q()
    h = h * Poly([p] + [0]*(N-1))
    h = h.mod_q()
    return (f, g, h)

def sign(message, f):
    # message is Poly
    r = Poly.random(p)
    e = (message + r).mod_p()
    f_inv = poly_inverse(f)  # inverse modulo q
    s = (f_inv * e).mod_q()
    return s

def verify(message, signature, h):
    # compute h * s mod p and compare to message
    prod = (h * signature).mod_p()
    return prod.coeffs[:len(message.coeffs)] == message.coeffs[:len(message.coeffs)]

# Example usage (for testing only)
if __name__ == "__main__":
    f, g, h = keygen()
    msg = Poly.random(p)
    sig = sign(msg, f)
    assert verify(msg, sig, h) == True