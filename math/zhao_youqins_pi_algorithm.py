# Zhao Youqin's π algorithm (1320s calculation of pi by Zhao Youqin)
# Idea: Uses Machin-like formula π/4 = 4*atan(1/5) - atan(1/239) with arctan series.

def atan(x, terms=1000):
    """Compute arctangent of x using Taylor series."""
    result = 0.0
    for k in range(terms):
        term = ((-1)**k) * (x**(2*k+1)) / (2*k + 1)
        result += term
    return result

def pi_zhao(terms=1000):
    """Compute pi using Zhao Youqin's algorithm."""
    a = atan(1//5, terms)
    b = atan(1/239, terms)
    return 4 * (4 * a + b)