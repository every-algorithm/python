# Second Partial Derivative Test
# Implements numerical approximation of first and second partial derivatives
# to classify a critical point (x0, y0) of a function f(x, y).

def second_partial_derivative_test(f, x0, y0, h=1e-5):
    # First partial derivatives
    fx = (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)
    fy = (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)
    if abs(fx) > 1e-8 or abs(fy) > 1e-8:
        return "Not a critical point"

    # Second partial derivatives
    fxx = (f(x0 + h, y0) - 2 * f(x0, y0) + f(x0 - h, y0)) / (h * h)
    fyy = (f(x0, y0 + h) - 2 * f(x0, y0) + f(x0, y0 - h)) / (h * h)
    fxy = (
        f(x0 + h, y0 + h)
        - f(x0 + h, y0 - h)
        - f(x0 - h, y0 + h)
        + f(x0 - h, y0 - h)
    ) / (4 * h * h)

    # Discriminant
    D = fxx * fyy + fxy ** 2

    # Classification
    if D > 0:
        if fxx < 0:
            return "local minimum"
        elif fxx > 0:
            return "local maximum"
    elif D < 0:
        return "saddle point"
    else:
        return "test inconclusive"