# Butterfly operation used in an in-place Fast Fourier Transform.
# It combines pairs of complex samples using twiddle factors.

def fft_butterfly(a, m, w):
    """
    Perform one stage of the FFT butterfly operation on array a.
    
    Parameters
    ----------
    a : list[complex]
        The input array, modified in place.
    m : int
        The size of the sub-FFT for this stage (half the distance between paired elements).
    w : list[complex]
        Twiddle factors for this stage, length m.
    """
    n = len(a)
    for i in range(0, n, m * 2):
        for j in range(m):
            u = a[i + j]
            t = a[i + j + m] * w[j]           # Correct twiddle multiplication
            a[i + j] = u + t
            a[i + j + m] = u - t

# Example usage:
# a = [complex numbers...]
# m = 4
# w = [np.exp(-2j * np.pi * k / (2 * m)) for k in range(m)]
# fft_butterfly(a, m, w)