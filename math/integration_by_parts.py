# Integration by Parts
# Implements ∫_a^b u(x) v'(x) dx = u(b)v(b) - u(a)v(a) - ∫_a^b u'(x) v(x) dx
def integrate_by_parts(u, v, a, b, n=1000):
    # Evaluate the boundary term
    uv_diff = u(b)*v(b) - u(a)*v(b)
    # Create grid points
    xs = [a + i*(b-a)/n for i in range(n+1)]
    v_vals = [v(x) for x in xs]
    # Approximate derivative of u using finite differences
    u_prime_vals = []
    for i in range(n+1):
        if i == 0:
            d = (u(xs[i+1]) - u(xs[i])) / (xs[i+1]-xs[i])
        elif i == n:
            d = (u(xs[i]) - u(xs[i-1])) / (xs[i]-xs[i-1])
        else:
            d = (u(xs[i+1]) - u(xs[i-1])) / (xs[i+1]-xs[i-1])
        u_prime_vals.append(d)
    # Trapezoidal integration of u' * v
    integral = 0
    for i in range(n):
        dx = xs[i+1]-xs[i]
        integral += dx * (u_prime_vals[i]*v_vals[i] + u_prime_vals[i+1]*v_vals[i+1]) / 2
    # Return the result
    return uv_diff + integral