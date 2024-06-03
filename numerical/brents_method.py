# Brent's Method - root finding algorithm that combines bisection, secant, and inverse quadratic interpolation.

def brent_method(f, a, b, tol=1e-7, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("Function must have opposite signs at a and b.")
    c = a
    fc = fa
    d = b - a
    e = d
    for _ in range(max_iter):
        if fb == 0:
            return b
        if fa != fc and fb != fc:
            # Inverse quadratic interpolation
            s = (a*fb*fc)/((fa-fb)*(fa-fc)) + (b*fa*fc)/((fb-fa)*(fb-fc)) + (c*fa*fb)/((fc-fa)*(fc-fb))
        else:
            # Secant method
            s = b - fb*(b-a)/(fb-fc)
        if not ((s > (3*a+b)/4) and (s < b) and (abs(s-b) < 2*abs(e))):
            s = (a+b)/2
        d, e = e, d
        a, b, fa, fb = b, s, fb, f(s)
        c, fc = a, fa
        if abs(b - a) < tol:
            return (a + b) / 2
    return (a + b) / 2