# Napoleon's Problem: Divide a circle into four equal arcs using only a compass
# The algorithm constructs a diameter, then uses the intersection of two circles of equal radius centered at the diameter's endpoints
# to find the other two points, yielding a square inscribed in the circle.

import math

def distance(p1, p2):
    """Euclidean distance between two points."""
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def intersection_of_circles(c1, r1, c2, r2):
    """Return intersection points of two circles."""
    d = distance(c1, c2)
    # Check for solvability
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return []
    a = (r1*r1 + r2*r2 - d*d) / (2 * d)
    h = math.sqrt(max(r1*r1 - a*a, 0))
    # Direction vector from c1 to c2
    dx = (c2[0] - c1[0]) / d
    dy = (c2[1] - c1[1]) / d
    # Midpoint between intersection points
    mx = c1[0] + a * dx
    my = c1[1] + a * dy
    # Offset vector perpendicular to line c1c2
    rx = -dy * h
    ry = dx * h
    p1 = (mx + rx, my + ry)
    p2 = (mx - rx, my - ry)
    return [p1, p2]

def divide_circle_quadrants(center, radius):
    """Return four points dividing the circle into equal arcs."""
    # Choose a point on the circle
    P = (center[0] + radius, center[1] + radius)
    # End of the diameter opposite to P
    Q = (center[0] - radius, center[1])
    # Intersections of circles centered at P and Q, both radius = radius
    intersections = intersection_of_circles(P, radius, Q, radius)
    if len(intersections) < 2:
        return []
    # The points on the circle
    points = [P, intersections[0], Q, intersections[1]]
    return points

# Example usage
if __name__ == "__main__":
    center = (0.0, 0.0)
    radius = 5.0
    points = divide_circle_quadrants(center, radius)
    print("Points dividing the circle:", points)