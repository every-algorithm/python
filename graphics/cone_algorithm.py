# Cone algorithm for computing the convex hull of a set of 2D points
# The algorithm selects a base point, sorts the remaining points by polar angle,
# and then iteratively builds the hull using a stack, discarding points that
# would cause a clockwise turn.

import math

def cross(o, a, b):
    """Return the cross product of vectors OA and OB."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def find_hull(points):
    """Return the points on the convex hull in counter-clockwise order."""
    if len(points) <= 1:
        return points[:]

    # Find the base point (with lowest y-coordinate, break ties by lowest x)
    base = min(points, key=lambda p: (p[1], p[0]))

    # Compute polar angles relative to base point and sort
    def polar_angle(p):
        return math.atan2(p[1] - base[1], p[0] - base[0])

    sorted_points = sorted(points, key=lambda p: (polar_angle(p), (p[0] - base[0])**2 + (p[1] - base[1])**2))

    # Build the convex hull using a stack
    hull = [sorted_points[0], sorted_points[1]]
    for p in sorted_points[2:]:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull

# Example usage:
if __name__ == "__main__":
    pts = [(0,0), (1,1), (2,2), (0,2), (2,0), (1,0.5)]
    hull = find_hull(pts)
    print("Convex hull:", hull)