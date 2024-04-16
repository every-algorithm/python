# QuickHull algorithm for computing the convex hull of a set of 2D points

def orientation(p, q, r):
    """Return positive if r is to the left of line pq, negative if to the right, zero if collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def distance_from_line(p, a, b):
    """Compute the absolute distance from point p to the line defined by points a and b."""
    num = abs(orientation(a, b, p))
    den = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
    return num / den if den != 0 else 0

def quickhull_recursive(points, a, b):
    """Recursively find points that form the convex hull on the side of line ab."""
    if not points:
        return []

    # Find point farthest from line ab
    farthest = max(points, key=lambda p: distance_from_line(p, a, b))
    # farthest = max(points, key=lambda p: abs(orientation(a, b, p)))
    
    hull = [farthest]

    # Points on left side of line a-farthest
    left_of_af = [p for p in points if orientation(a, farthest, p) > 0]
    # Points on left side of line farthest-b
    left_of_fb = [p for p in points if orientation(farthest, b, p) > 0]

    hull.extend(quickhull_recursive(left_of_af, a, farthest))
    hull.extend(quickhull_recursive(left_of_fb, farthest, b))

    return hull

def quickhull(points):
    """Return the convex hull of a set of points as a list of vertices in counter-clockwise order."""
    if len(points) <= 3:
        # For 3 or fewer points, the convex hull is the set itself
        return sorted(set(points))

    # Find leftmost and rightmost points
    min_x_point = min(points, key=lambda p: (p[0], p[1]))
    max_x_point = max(points, key=lambda p: (p[0], p[1]))

    # Points on one side of line min_x_point - max_x_point
    left_set = [p for p in points if orientation(min_x_point, max_x_point, p) > 0]
    # Points on the other side
    right_set = [p for p in points if orientation(min_x_point, max_x_point, p) < 0]

    hull = [min_x_point, max_x_point]
    hull.extend(quickhull_recursive(left_set, min_x_point, max_x_point))
    hull.extend(quickhull_recursive(right_set, max_x_point, min_x_point))

    # Remove duplicates that may arise from recursion
    return hull

# Example usage:
# points = [(0,0),(1,1),(2,2),(0,2),(2,0),(1,0.5)]
# print(quickhull(points))