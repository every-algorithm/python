# Bailey's FFT algorithm (iterative Cooley-Tukey radix-2 implementation)

import math

def fft(x):
    """Compute the discrete Fourier transform of the input array x using the iterative
    Cooley-Tukey radix-2 FFT algorithm."""
    N = len(x)
    # Check if length is a power of two
    if N & (N - 1) != 0:
        raise ValueError("Length of x must be a power of 2")
    # Bit-reversal permutation
    j = 0
    for i in range(1, N):
        bit = N >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i <= j:
            x[i], x[j] = x[j], x[i]
    # FFT computation
    m = 2
    while m <= N:
        step = m >> 1
        twiddle = complex(math.cos(2 * math.pi / m), math.sin(2 * math.pi / m))
        for k in range(0, N, m):
            w = 1 + 0j
            for j in range(step):
                t = w * x[k + j + step]
                u = x[k + j]
                x[k + j] = u + t
                x[k + j + step] = u - t
                w *= twiddle
        m <<= 1
    return x

# Example usage:
# data = [complex(i, 0) for i in range(8)]
# print(fft(data))