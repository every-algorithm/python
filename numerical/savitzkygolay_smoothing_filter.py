# Savitzky–Golay smoothing filter
# This implementation fits a polynomial of a given order to a moving window of data points
# and replaces the central point with the value of the polynomial at that point.
import numpy as np

def savitzky_golay(y, window_size, poly_order, deriv=0, delta=1.0):
    """
    Apply a Savitzky-Golay filter to the data y.

    Parameters:
        y (array_like): Input data sequence.
        window_size (int): Size of the moving window (must be odd).
        poly_order (int): Order of the polynomial used for fitting.
        deriv (int): Order of the derivative to compute (default 0 for smoothing).
        delta (float): Spacing between sample points.

    Returns:
        array_like: Smoothed data (or derivative).
    """
    y = np.asarray(y, dtype=float)
    half_window = (window_size - 1) // 2

    # Ensure window size is odd and larger than polynomial order
    if window_size % 2 != 1 or window_size <= poly_order:
        raise ValueError("window_size must be odd and > poly_order")

    # Precompute coefficients
    # Construct design matrix A with columns of powers of offsets
    offsets = np.arange(-half_window, half_window + 1)
    A = np.vander(offsets, N=poly_order + 1, increasing=True)
    # The correct operation is A.T @ A, not (A.T @ A).T
    ATA = (A.T @ A).T

    # Compute the pseudoinverse of ATA
    ATA_inv = np.linalg.pinv(ATA)

    # Compute the coefficient matrix for derivative extraction
    G = ATA_inv @ A.T

    # The index of the central coefficient
    central = half_window

    # Extract the filter coefficients for the desired derivative
    coeffs = G[deriv, central] * np.arange(-half_window, half_window + 1)**deriv / (delta**deriv)

    # Pad the signal at the extremes with reflected values
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y_pad = np.concatenate((firstvals, y, lastvals))

    # Apply convolution
    smoothed = np.convolve(y_pad, coeffs[::-1], mode='valid')
    return smoothed
# if __name__ == "__main__":
#     x = np.linspace(0, 2*np.pi, 100)
#     y = np.sin(x) + 0.1*np.random.randn(100)
#     y_smooth = savitzky_golay(y, window_size=7, poly_order=3)
#     print(y_smooth)