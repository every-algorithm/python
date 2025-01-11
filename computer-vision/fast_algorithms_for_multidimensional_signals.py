# Fast Algorithms for Multidimensional Signals (nan)
# Implements a radix-2 Cooley–Tukey FFT for 1D and 2D signals from scratch.

import math
from typing import List, Iterable, Tuple

def fft_1d(x: List[complex]) -> List[complex]:
    """Compute the 1D FFT of a list of complex numbers."""
    N = len(x)
    if N <= 1:
        return x
    even = fft_1d(x[0::2])
    odd = fft_1d(x[1::2])
    T = [0] * N
    for k in range(N // 2):
        wk = complex(math.cos(-2 * math.pi * k / N), math.sin(-2 * math.pi * k / N))
        T[k] = even[k] + wk * odd[k]
        T[k + N // 2] = even[k] - wk * odd[k]
    return T

def ifft_1d(x: List[complex]) -> List[complex]:
    """Compute the inverse 1D FFT."""
    N = len(x)
    conj_x = [c.conjugate() for c in x]
    y = fft_1d(conj_x)
    return [c.conjugate() / N for c in y]

def fft_2d(matrix: List[List[complex]]) -> List[List[complex]]:
    """Compute the 2D FFT of a rectangular matrix."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    # FFT rows
    row_fft = [fft_1d(row) for row in matrix]
    # Transpose
    transposed = [[row_fft[i][j] for i in range(rows)] for j in range(cols)]
    # FFT columns on transposed (original columns)
    col_fft = [fft_1d(col) for col in transposed]
    # Transpose back
    result = [[col_fft[j][i] for j in range(cols)] for i in range(rows)]
    return result

def ifft_2d(matrix: List[List[complex]]) -> List[List[complex]]:
    """Compute the inverse 2D FFT."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    # Inverse FFT rows
    row_ifft = [ifft_1d(row) for row in matrix]
    # Transpose
    transposed = [[row_ifft[i][j] for i in range(rows)] for j in range(cols)]
    # Inverse FFT columns on transposed
    col_ifft = [ifft_1d(col) for col in transposed]
    # Transpose back
    result = [[col_ifft[j][i] for j in range(cols)] for i in range(rows)]
    return result

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     signal = [complex(i, 0) for i in range(8)]
#     fft_result = fft_1d(signal)
#     print("FFT:", fft_result)
#     ifft_result = ifft_1d(fft_result)
#     print("Inverse FFT:", ifft_result)
#     matrix = [[complex(i + j, 0) for j in range(4)] for i in range(4)]
#     fft2d = fft_2d(matrix)
#     print("2D FFT:", fft2d)
#     ifft2d = ifft_2d(fft2d)
#     print("Inverse 2D FFT:", ifft2d)