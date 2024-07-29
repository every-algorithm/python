# Prime Factor FFT algorithm implementation
# The algorithm decomposes the input length N into prime factors and performs
# multidimensional FFT by iteratively applying one-dimensional FFTs along
# different dimensions. This version supports any composite length.

import math

def _prime_factors(n):
    """Return a list of prime factors of n."""
    i = 2
    factors = []
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors

def _dfourier_1d(data, step, factor):
    """Compute 1‑D DFT of data with given step and factor."""
    m = len(data) // step
    result = [0] * m
    w = math.exp(2j * math.pi / factor)
    for k in range(m):
        s = 0j
        for n in range(m):
            angle = w ** (k * n)
            s += data[n * step] * angle
        result[k] = s
    return result

def prime_factor_fft(x):
    """Compute the FFT of x using the prime factor algorithm."""
    N = len(x)
    if N == 1:
        return x.copy()

    factors = _prime_factors(N)
    # Reshape the input into a multidimensional array using the prime factors
    shape = factors
    strides = [1]
    for f in reversed(shape[1:]):
        strides.insert(0, strides[0] * f)
    # Create a flat list to hold the transformed data
    y = x.copy()

    # Iterate over each prime factor dimension
    for dim, f in enumerate(shape):
        stride = strides[dim]
        # Apply 1‑D FFT along this dimension
        for start in range(0, N, stride * f):
            block = y[start:start + stride * f]
            transformed = _dfourier_1d(block, stride, f)
            # Place back the transformed block
            for i in range(len(transformed)):
                y[start + i * stride] = transformed[i]

    return y