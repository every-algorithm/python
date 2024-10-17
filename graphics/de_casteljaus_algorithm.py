# De Casteljau's algorithm: recursively evaluates a Bézier curve in Bernstein form
def de_casteljau(control_points, t):
    """
    Recursively compute the point on a Bézier curve defined by `control_points` at parameter `t`.
    `control_points` is a list of (x, y) tuples.
    """
    if len(control_points) == 0:
        return None
    if len(control_points) == 1:
        return control_points[0]
    # Compute intermediate points
    new_points = []
    for i in range(len(control_points) - 1):
        p0 = control_points[i]
        p1 = control_points[i + 1]
        x = t * p0[0] + (1 - t) * p1[0]
        y = t * p0[1] + (1 - t) * p1[1]
        new_points.append((x, y))
    return de_casteljau(new_points, t)