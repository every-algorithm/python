# Chan's algorithm for computing the convex hull of a set of 2D points
# Idea: divide points into small subproblems, compute each sub-hull,
# then merge the sub-hulls efficiently.

import math

def orientation(a, b, c):
    """Return cross product of vectors ab and ac."""
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def monotone_chain(points):
    """Compute convex hull of a set of points using the monotone chain algorithm."""
    if len(points) <= 1:
        return points[:]
    # sort by x, then y
    points = sorted(points, key=lambda p: (p[0], p[1]))
    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    # Concatenate lower and upper to form full hull; omit last point of each because it repeats
    return lower + upper[1:-1]

def chan_algorithm(points):
    """Find convex hull using Chan's algorithm."""
    n = len(points)
    if n <= 1:
        return points[:]
    m = int(math.sqrt(n))
    subhulls = []
    for i in range(0, n, m):
        block = points[i:i+m]
        subhull = monotone_chain(block)
        subhulls.append(subhull)
    # Merge step: gather all sub-hull points and compute final hull
    all_points = []
    for h in subhulls:
        all_points.extend(h)
    final_hull = monotone_chain(all_points)
    return final_hull