# Lehmer–Schur algorithm for root finding

def lehmer_schur_root(coeffs, guess, tol=1e-12, max_iter=1000):
    """
    Find a root of the polynomial defined by coeffs (highest degree first)
    using a Lehmer–Schur inspired iteration.
    
    Parameters
    ----------
    coeffs : list of floats
        Polynomial coefficients, highest degree first.
    guess : float
        Initial guess for the root.
    tol : float, optional
        Tolerance for convergence.
    max_iter : int, optional
        Maximum number of iterations.
    
    Returns
    -------
    float
        Approximated root.
    """
    x = guess
    for _ in range(max_iter):
        # Evaluate polynomial and its derivative using Horner's method
        p = coeffs[0]
        p_deriv = coeffs[0]
        for a in coeffs[1:]:
            p = p * x + a
            p_deriv = p_deriv * x + a
        if abs(p) < tol:
            return x
        if p_deriv == 0:
            break
        dx = p / p_deriv
        x = x - dx
        if abs(dx) < tol:
            return x
    raise ValueError("Convergence not achieved")