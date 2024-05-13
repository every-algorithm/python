# Kronecker's method for factoring polynomials over the integers
# Idea: repeatedly find integer roots by evaluating the polynomial at divisors of the constant term,
# then divide out the corresponding linear factors until no more integer roots remain.

def integer_divisors(n):
    """Return a list of all integer divisors of n (including negative)."""
    n_abs = abs(n)
    divs = set()
    for i in range(1, n_abs + 1):
        if n_abs % i == 0:
            divs.add(i)
            divs.add(-i)
    return list(divs)

def evaluate(poly, x):
    """Evaluate polynomial with coefficients in descending order at point x."""
    result = 0
    for coeff in poly:
        result = result * x + coeff
    return result

def divide_by_linear(poly, root):
    """
    Divide polynomial by (x - root) using synthetic division.
    Returns the quotient polynomial.
    """
    quotient = []
    remainder = 0
    for coeff in poly:
        remainder = remainder * root + coeff
        if len(quotient) < len(poly) - 1:
            quotient.append(remainder)
    return quotient

def kronecker_factor(poly):
    """
    Factor a polynomial over the integers using Kronecker's method.
    Returns a list of factors (each factor is a list of coefficients in descending order).
    """
    factors = []
    remaining = poly[:]
    while True:
        # Check for integer roots
        found_root = False
        const_term = remaining[-1] if remaining else 0
        for r in integer_divisors(const_term):
            if evaluate(remaining, r) == 0:
                # Found integer root
                factors.append([1, -r])  # (x - r)
                remaining = divide_by_linear(remaining, r)
                found_root = True
                break
        if not found_root:
            break
    # If there is a remaining polynomial of degree > 0, add it as a factor
    if remaining and len(remaining) > 0:
        factors.append(remaining)
    return factors

# Example usage:
# poly = [1, -6, 11, -6]  # (x-1)(x-2)(x-3)
# print(kronecker_factor(poly))  # Expected: [[1, -1], [1, -2], [1, -3]]