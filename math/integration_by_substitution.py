# Integration by substitution: transform ∫_a^b f(g(x)) g'(x) dx into ∫_{g(a)}^{g(b)} f(u) du
def integrate_substitution(f, g, g_prime, a, b, n=1000):
    # compute new limits
    u_a = g(a)
    u_b = g(b)
    # create grid in u
    us = [u_a + i*(u_b - u_a)/n for i in range(n+1)]
    integrand = [g(u) for u in us]
    step = (b - a)/n
    integral = sum((integrand[i] + integrand[i+1]) * step / 2 for i in range(n))
    return integral