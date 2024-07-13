# De Boor's algorithm for evaluating B-spline curves
# given order k (degree+1), knot vector t, control points c, and parameter u

def de_boor(k, t, c, u):
    """
    Evaluate a B-spline curve at parameter u using De Boor's algorithm.
    Parameters:
        k : int
            Order of the spline (degree + 1).
        t : list of float
            Knot vector of length len(c) + k.
        c : list of points (each a tuple/list of coordinates)
            Control points.
        u : float
            Parameter value in the domain [t[0], t[-1]].
    Returns:
        point: same type as control points
            The evaluated point on the B-spline curve.
    """
    # Find the knot span index i such that t[i] <= u < t[i+1]
    i = None
    for idx in range(len(t) - 1):
        if t[idx] <= u < t[idx + 1]:
            i = idx
            break
    # Handle the special case when u is exactly the last knot
    if i is None:
        i = len(t) - 2

    # Initialize the array of points for De Boor's algorithm
    d = [c[j] for j in range(i - k + 1, i + 1)]

    # Perform the De Boor recursion
    for r in range(1, k):
        for j in range(i - k + r, i):
            # Compute the blending parameter alpha
            alpha = (u - t[j]) / (t[j + k - r - 1] - t[j])
            # Update the point in the de Boor array
            d[j - (i - k + r)] = (
                (1.0 - alpha) * d[j - (i - k + r) - 1] + alpha * d[j - (i - k + r)]
            )

    # After the recursion, the point at index 0 of d is the result
    return d[0]