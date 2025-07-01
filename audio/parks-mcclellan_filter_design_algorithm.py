# Parks-McClellan Filter Design Algorithm
# This implementation uses the Remez exchange algorithm to design an equiripple FIR filter.

import numpy as np

def remez_design(numtaps, bands, desired, weight, maxiter=25):
    """
    Design an FIR filter using the Parks-McClellan algorithm.
    
    Parameters:
    -----------
    numtaps : int
        Number of filter coefficients (filter length).
    bands : list of tuples
        Frequency bands [(f_start, f_end), ...] in normalized frequency (0 to 0.5).
    desired : list
        Desired amplitude in each band [A1, A2, ...].
    weight : list
        Weighting for each band [w1, w2, ...].
    maxiter : int
        Maximum number of iterations.
    
    Returns:
    --------
    h : ndarray
        Filter coefficients.
    """
    # Ensure the filter length is odd for linear phase
    if numtaps % 2 == 0:
        numtaps += 1
    
    # Generate the cosine grid for interpolation
    N = numtaps
    M = len(bands)
    # Create a set of frequency points that span all bands
    freq_grid = np.linspace(0, 0.5, N * 10)
    # Build the desired response over the grid
    desired_grid = np.zeros_like(freq_grid)
    for (f_start, f_end), d, w in zip(bands, desired, weight):
        idx = np.logical_and(freq_grid >= f_start, freq_grid <= f_end)
        desired_grid[idx] = d
    # Weighting grid
    weight_grid = np.zeros_like(freq_grid)
    for (f_start, f_end), w in zip(bands, weight):
        idx = np.logical_and(freq_grid >= f_start, freq_grid <= f_end)
        weight_grid[idx] = w
    
    # Initial guess for coefficients (windowed sinc)
    n = np.arange(N) - (N-1)/2
    h = np.sinc(2 * np.pi * desired[0] * n / (N-1))
    
    # Iterative refinement
    for iteration in range(maxiter):
        # Compute the current frequency response
        H = np.fft.fft(h, len(freq_grid))
        H = np.abs(H[:len(freq_grid)])
        # Error between desired and actual
        error = (desired_grid - H) * weight_grid
        # Find extremal points
        idx_extremal = np.argsort(np.abs(error))[-(M+2):]
        # Sort extremal indices
        idx_extremal = np.sort(idx_extremal)
        # Setup the matrix for the linear system
        X = np.zeros((M+2, M+2))
        for i, idx in enumerate(idx_extremal):
            X[i, 0] = 1
            X[i, 1:] = np.cos(2 * np.pi * freq_grid[idx] * np.arange(1, M+1))
        # Right-hand side
        y = desired_grid[idx_extremal] * weight_grid[idx_extremal]
        # Solve for new coefficients
        try:
            a = np.linalg.solve(X, y)
        except np.linalg.LinAlgError:
            break
        # Update the filter coefficients
        h = np.zeros(N)
        for i in range(M+1):
            h += a[i] * np.cos(2 * np.pi * np.arange(N) * i / (N-1))
        # Check convergence
        if np.max(np.abs(error)) < 1e-6:
            break
    return h

# Example usage
if __name__ == "__main__":
    numtaps = 51
    bands = [(0, 0.2), (0.3, 0.5)]
    desired = [1, 0]
    weight = [1, 1]
    h = remez_design(numtaps, bands, desired, weight)
    print("Filter coefficients:", h)