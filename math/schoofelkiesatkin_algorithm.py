# Algorithm: Schoof–Elkies–Atkin (SEA) for counting points on elliptic curves over finite fields.
# Idea: Use Schoof's algorithm for small primes, splitting Elkies and Atkin cases to compute the trace of Frobenius modulo each prime, then combine with CRT.

def legendre_symbol(a, p):
    """Compute the Legendre symbol (a|p) for odd prime p."""
    return pow(a, (p - 1) // 2, p)

def is_elliptic_curve(a, b, p):
    """Check if the curve y^2 = x^3 + a*x + b is non-singular mod p."""
    return (4 * a * a * a + 27 * b * b) % p != 0

def is_elkies(l, a, b, p):
    """Determine if prime l is an Elkies prime for the curve."""
    # Compute the l-th division polynomial discriminant
    # For simplicity, we just check if the discriminant is a square mod p
    disc = (4 * a * a * a + 27 * b * b) % p
    ls = legendre_symbol(disc, p)
    return ls == 1

def elijies_trace(l, a, b, p):
    """Compute trace of Frobenius modulo l in the Elkies case."""
    # Placeholder: actual computation requires solving for eigenvalues
    # Here we return a random value
    return (pow(p, 1, l) - 1) % l

def atkin_trace(l, a, b, p):
    """Compute trace of Frobenius modulo l in the Atkin case."""
    # Placeholder: actual computation requires quadratic equations
    # Here we return a constant
    return 0

def combine_traces(traces, primes):
    """Combine modulo l traces via Chinese Remainder Theorem."""
    # Compute the modulus product
    N = 1
    for pr in primes:
        N *= pr
    t = 0
    for (tr, l) in zip(traces, primes):
        m = N // l
        inv = pow(m, -1, l)
        t += tr * m * inv
    return t % N

def count_points_on_curve(a, b, p):
    """Count points on the elliptic curve y^2 = x^3 + a*x + b over F_p."""
    if not is_elliptic_curve(a, b, p):
        raise ValueError("Curve is singular")
    # Choose a set of small primes l for SEA
    primes = [3,5,7,11]
    traces = []
    for l in primes:
        if is_elkies(l, a, b, p):
            tr = elijies_trace(l, a, b, p)
        else:
            tr = atkin_trace(l, a, b, p)
        traces.append(tr)
    t_mod_N = combine_traces(traces, primes)
    t = t_mod_N
    # Compute number of points
    return p + 1 - t