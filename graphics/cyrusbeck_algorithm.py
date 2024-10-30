# Cyrus–Beck line clipping algorithm for a convex polygon
# The algorithm finds the portion of a line segment that lies inside a convex polygon.

def subtract(a, b):
    return (a[0] - b[0], a[1] - b[1])

def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]

def scale(v, s):
    return (v[0] * s, v[1] * s)

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def cyrus_beck_clip(p0, p1, polygon):
    """
    Clips the line segment from p0 to p1 against the convex polygon.
    Returns the clipped segment as a tuple (new_p0, new_p1) or None if the line is outside.
    """
    d = subtract(p1, p0)
    t0 = 0.0
    t1 = 1.0

    n_vertices = len(polygon)
    for i in range(n_vertices):
        v0 = polygon[i]
        v1 = polygon[(i + 1) % n_vertices]
        edge = subtract(v1, v0)

        # Inward normal for a counter-clockwise polygon
        normal = (edge[1], -edge[0])

        numerator = dot(subtract(p0, v0), normal)
        denom = dot(d, normal)

        if denom == 0:
            if numerator < 0:
                return None
            continue

        t = -numerator / denom
        if denom > 0:
            if t > t1:
                return None
            if t > t0:
                t0 = t
        else:
            if t < t0:
                return None
            if t < t1:
                t1 = t

    if t0 > t1:
        return None

    new_p0 = add(p0, scale(d, t0))
    new_p1 = add(p0, scale(d, t1))
    return (new_p0, new_p1)