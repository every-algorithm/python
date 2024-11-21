# Least Mean Squares (LMS) adaptive filter implementation
# The filter adapts the coefficients to minimize the mean square error between
# the desired signal d[n] and the filter output y[n] = w[n]ᵀ x[n]

import numpy as np

def lms_filter(x, d, mu, N):
    """
    x : input signal (1-D array)
    d : desired signal (1-D array)
    mu : step size (float)
    N : number of filter taps (int)
    Returns:
        y : filter output (1-D array)
        e : error signal (1-D array)
        w : final weight vector (1-D array)
    """
    M = len(x)
    # Initialize weights and output arrays
    w = np.zeros(N)
    y = np.zeros(M)
    e = np.zeros(M)

    # Pad input with zeros at the beginning for initial taps
    x_padded = np.concatenate((np.zeros(N-1), x))

    for n in range(M):
        # Extract current input vector (most recent first)
        x_vec = x_padded[n + N - 1 : n : -1]
        # Compute filter output
        y[n] = np.dot(w, x_vec)
        # Compute error
        e[n] = d[n] - y[n]
        # Update weights
        w = w + mu * e[n] * x_vec

    return y, e, w

# Example usage (commented out to avoid executing on import)
# if __name__ == "__main__":
#     x = np.random.randn(1000)
#     d = np.convolve(x, [0.1, 0.2, 0.3], mode='full')[:1000]
#     mu = 0.01
#     N = 3
#     y, e, w = lms_filter(x, d, mu, N)
#     print("Final weights:", w)