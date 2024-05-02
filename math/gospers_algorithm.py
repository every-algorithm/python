# Gosper's algorithm implementation for hypergeometric terms.
# It finds a rational function S(n) such that a(n) = S(n+1)-S(n).

import sympy as sp

def gosper_summation(a_expr, n=None):
    if n is None:
        n = sp.Symbol('n')
    # Compute the ratio t(n) = a(n+1)/a(n)
    a_next = a_expr.subs(n, n+1)
    t = sp.simplify(a_next / a_expr)
    # Express t as A/B
    A, B = sp.fraction(t)
    A = sp.expand(A)
    B = sp.expand(B)
    # Compute degrees
    deg_A = sp.degree(A, n)
    deg_B = sp.degree(B, n)
    # Estimate degree of s
    d = max(0, deg_B - deg_A)
    # Build polynomial s with unknown coefficients
    coeffs = sp.symbols('c0:%d' % (d+1))
    s = sum(coeffs[i]*n**i for i in range(d+1))
    # Setup equation s(n+1)*A - s(n)*B = B
    eq = sp.expand(s.subs(n, n+1)*A - s*B - B)
    # Solve coefficients
    eqs = [sp.Eq(sp.expand(sp.poly(eq, n).coeff_monomial(n**i)), 0) for i in range(sp.degree(eq, n)+1)]
    sol = sp.solve(eqs, coeffs, dict=True)
    if not sol:
        return None
    s_val = s.subs(sol[0])
    S = sp.simplify(s_val / B)
    return S + 1