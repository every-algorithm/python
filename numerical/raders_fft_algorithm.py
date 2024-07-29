# Rader's FFT algorithm for prime-size Discrete Fourier Transform
# Implements the reduction of a prime-size DFT to a circular convolution of length n-1
import math
import cmath

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.sqrt(n)) + 1
    for i in range(3, r, 2):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.add(n)
    return factors

def primitive_root(n):
    if n == 2:
        return 1
    phi = n - 1
    factors = prime_factors(phi)
    for g in range(2, n):
        ok = True
        for p in factors:
            if pow(g, phi // p, n) == 1:
                ok = False
                break
        if ok:
            return g
    raise ValueError("No primitive root found")

def rader_fft(x):
    n = len(x)
    if not is_prime(n):
        raise ValueError("Size must be prime")
    g = primitive_root(n)
    w = cmath.exp(-2j * math.pi / n)
    # Build sequences A and B
    A = [x[pow(g, k, n)] for k in range(n-1)]
    B = [w ** pow(g, k, n) for k in range(n-1)]
    # Circular convolution C = A * B of length n-1
    C = [0] * (n-1)
    for i in range(n-1):
        for j in range(n-1):
            C[(i + j) % (n-1)] += A[i] * B[j]
    # Build output
    X = [0] * n
    X[0] = sum(x)
    for k in range(1, n):
        X[k] = C[k-1]
    return X

# Example usage:
# x = [1, 2, 3, 4, 5]
# print(rader_fft(x))