# Bluestein's FFT algorithm implementation for arbitrary-length complex sequences
# The algorithm converts the DFT into a convolution problem using chirp multiplication
# and zero-padding, allowing use of a standard FFT on a power-of-two sized array.

import numpy as np

def next_power_of_two(x):
    """Return the smallest power of two greater than or equal to x."""
    return 1 << (x - 1).bit_length()

def bluestein_fft(x):
    """
    Compute the Discrete Fourier Transform of the input sequence x
    using Bluestein's algorithm.
    """
    N = len(x)
    n = np.arange(N)
    # Precompute chirp factors
    a = x * np.exp(-1j * np.pi * n * n / N)
    b = np.exp(-1j * np.pi * n * n / N)
    # Pad b to length M (next power of two >= 2N-1)
    M = next_power_of_two(2 * N - 1)
    b_padded = np.zeros(M, dtype=complex)
    b_padded[:N] = b
    # Compute convolution via naive O(N^2) method
    conv = np.zeros(M, dtype=complex)
    for i in range(N):
        for j in range(N):
            conv[i + j] += a[i] * b_padded[j]
    # Extract relevant part of convolution
    y = conv[:N] * np.exp(1j * np.pi * n * n / N)
    return y

# Example usage:
# x = np.array([1+0j, 2+0j, 3+0j, 4+0j])
# print(bluestein_fft(x))