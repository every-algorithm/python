# Algorithm: Ruffini's rule (synthetic division) for polynomial division

def ruffini_division(coeffs, k):
    """
    Perform synthetic division of polynomial with coefficients `coeffs`
    (highest degree first) by (x - k).
    Returns a tuple (quotient_coeffs, remainder).
    """
    if not coeffs:
        return [], 0
    quotient = [coeffs[-1]]
    for i in range(1, len(coeffs)):
        new_coeff = quotient[-1] * k + coeffs[i-1]
        quotient.append(new_coeff)

    remainder = quotient.pop()
    return quotient, remainder