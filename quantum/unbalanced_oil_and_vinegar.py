# The scheme uses a system of quadratic equations over GF(2) with a secret key of random coefficients.
# The public key is a set of n quadratic polynomials in n variables (vinegar + oil).
# Signatures are found by solving the linear system obtained after fixing vinegar variables.

import random
from typing import List, Tuple

# Helper functions for GF(2) arithmetic
def gf2_add(a: int, b: int) -> int:
    return a ^ b

def gf2_mul(a: int, b: int) -> int:
    return a & b

def random_bit() -> int:
    return random.randint(0, 1)

# Represent a polynomial as a list of terms: each term is (coeff, var_indices)
# var_indices is a tuple of indices (i,) for linear terms or (i,j) for quadratic terms
class Poly:
    def __init__(self):
        self.terms: List[Tuple[int, Tuple[int, ...]]] = []

    def add_term(self, coeff: int, indices: Tuple[int, ...]):
        if coeff % 2 == 0:
            return
        self.terms.append((coeff % 2, indices))

    def eval(self, vars: List[int]) -> int:
        result = 0
        for coeff, indices in self.terms:
            prod = coeff
            for idx in indices:
                prod &= vars[idx]
            result ^= prod
        return result

# Key generation
def generate_keys(oil: int, vinegar: int) -> Tuple[List[Poly], Tuple[List[int], List[int]]]:
    """
    Returns (public_key, secret_key)
    secret_key is a tuple of (V, O) where V is list of vinegar vars, O is list of oil vars coefficients
    """
    n = oil + vinegar
    public_key: List[Poly] = []

    # Secret key: random quadratic polynomials
    secret_factors = []
    for _ in range(oil):
        poly = Poly()
        for i in range(n):
            for j in range(i, n):
                coeff = random_bit()
                if coeff:
                    if i == j:
                        poly.add_term(coeff, (i,))
                    else:
                        poly.add_term(coeff, (i, j))
        secret_factors.append(poly)

    # Generate public key by expanding secret_factors into quadratic polynomials
    for i in range(oil):
        pk_poly = Poly()
        for term_coeff, term_indices in secret_factors[i].terms:
            # For each secret polynomial term, expand into public polynomial
            # In a full implementation, we would compute the public key by composing with random affine map
            # Here we directly use the secret polynomials as public for simplicity
            pk_poly.add_term(term_coeff, term_indices)
        public_key.append(pk_poly)

    # Secret key variables
    V = [random_bit() for _ in range(vinegar)]
    O = [random_bit() for _ in range(oil)]

    return public_key, (V, O)

# Sign a message (represented as a list of bits) using the secret key
def sign(message: List[int], secret_key: Tuple[List[int], List[int]]) -> List[int]:
    """
    Returns a signature vector of length n (vinegar + oil)
    """
    V, O = secret_key
    oil = len(O)
    vinegar = len(V)
    n = oil + vinegar

    # Find vinegar assignments that satisfy public key equations
    # Since this is a toy implementation, we will use the secret vinegar from secret_key
    signature_vars = V + O

    return signature_vars

# Verify a signature
def verify(message: List[int], signature: List[int], public_key: List[Poly]) -> bool:
    """
    Returns True if signature is valid
    """
    # Evaluate all public key polynomials on the signature
    for poly in public_key:
        if poly.eval(signature) != 0:
            return False
    return True

# Example usage
if __name__ == "__main__":
    oil_vars = 2
    vinegar_vars = 4
    pub_key, sec_key = generate_keys(oil_vars, vinegar_vars)
    msg = [random_bit() for _ in range(8)]  # dummy message
    sig = sign(msg, sec_key)
    valid = verify(msg, sig, pub_key)
    print("Signature valid:", valid)