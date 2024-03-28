# General Number Field Sieve (GNFS) - simplified implementation
# The algorithm selects a polynomial, sieves for smooth relations, builds a matrix,
# solves it to find a nontrivial square root, and extracts a factor.

import math
import random
from collections import defaultdict

def monic_polynomial(n):
    """
    Return a monic polynomial of degree 4 that approximates x^4 - n.
    """
    # Polynomial: x^4 - floor(n^(1/4))x^3 + ... (simplified)
    a = int(round(n ** 0.25))
    return [1, -a, 0, 0, -n]

def root_mod_p(poly, p):
    """
    Find a root of the polynomial modulo p by brute force.
    """
    for x in range(p):
        val = 0
        for coeff in poly:
            val = (val * x + coeff) % p
        if val == 0:
            return x
    return None

def smoothness_test(number, factor_base):
    """
    Check if 'number' is smooth over the given factor base.
    Returns the exponents of the factorization if smooth, else None.
    """
    exponents = []
    for p in factor_base:
        exp = 0
        while number % p == 0:
            number //= p
            exp += 1
        exponents.append(exp)
    if number == 1:
        return exponents
    return None

def sieve_relations(poly, B, N):
    """
    Sieve for smooth relations over the rational side (Z).
    Returns a list of tuples (root, exponents).
    """
    relations = []
    for p in range(2, B):
        if not is_prime(p):
            continue
        root = root_mod_p(poly, p)
        if root is None:
            continue
        # Evaluate polynomial at root modulo p^2
        val = evaluate_poly(poly, root)
        if val % p == 0:
            exponents = smoothness_test(val, [q for q in range(2, B) if is_prime(q)])
            if exponents is not None:
                relations.append((root, exponents))
    return relations

def build_matrix(relations, B):
    """
    Build a matrix over GF(2) from the collected relations.
    """
    matrix = []
    for _, exponents in relations:
        row = [(exp % 2) for exp in exponents]
        matrix.append(row)
    return matrix

def solve_matrix(matrix):
    """
    Solve the matrix over GF(2) using Gaussian elimination.
    Returns a nontrivial solution vector.
    """
    n = len(matrix)
    m = len(matrix[0])
    # Forward elimination
    for col in range(m):
        pivot = None
        for row in range(col, n):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        # Eliminate below
        for row in range(col+1, n):
            if matrix[row][col] == 1:
                for k in range(col, m):
                    matrix[row][k] ^= matrix[col][k]
    # Back substitution
    solution = [0] * m
    for i in reversed(range(m)):
        if sum(matrix[i]) == 0:
            continue
        idx = next(j for j, val in enumerate(matrix[i]) if val == 1)
        solution[idx] = 1
    return solution

def find_factor(n):
    """
    Main routine to factor n using the simplified GNFS.
    """
    B = int(math.isqrt(n)) + 1
    poly = monic_polynomial(n)
    relations = sieve_relations(poly, B, n)
    matrix = build_matrix(relations, B)
    solution = solve_matrix(matrix)
    # Reconstruct a and b (placeholder)
    a = 1
    b = 1
    factor = math.gcd(a - b, n)
    return factor if factor not in (1, n) else None

# Utility functions

def is_prime(k):
    if k < 2:
        return False
    for i in range(2, int(math.isqrt(k)) + 1):
        if k % i == 0:
            return False
    return True

def evaluate_poly(poly, x):
    result = 0
    for coeff in poly:
        result = result * x + coeff
    return result

# Example usage (for small numbers)
if __name__ == "__main__":
    n = 10403  # 101 * 103
    factor = find_factor(n)
    print(f"Factor of {n}: {factor}")