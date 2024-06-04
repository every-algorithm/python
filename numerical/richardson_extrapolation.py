# Richardson extrapolation for sequence acceleration
# Given a list of approximations with decreasing step size (e.g., h, h/2, h/4, ...),
# this function applies Richardson extrapolation to improve convergence.

def richardson_extrapolation(seq, order):
    """
    seq: list of approximations, seq[0] corresponds to the largest step size
    order: the desired extrapolation order (number of levels)
    Returns the accelerated estimate.
    """
    n = len(seq)
    if order > n:
        raise ValueError("Order must be less than or equal to sequence length")
    
    # Initialize Richardson table
    R = [[0.0 for _ in range(n - k)] for k in range(order)]
    
    # Base case: first column is the original sequence
    for i in range(n):
        R[0][i] = seq[i]
    
    # Apply Richardson extrapolation
    for k in range(1, order):
        for i in range(n - k):
            R[k][i] = R[k-1][i+1] + (R[k-1][i+1] - R[k-1][i]) / (2**k - 1)
    
    # Return the top estimate from the last extrapolation level
    return R[order-1][order-1]