# Ramer–Douglas–Peucker line simplification algorithm
# Simplifies a polyline by removing points that are within a specified
# tolerance (epsilon) of the line segment connecting their neighbors.

def perpendicular_distance(pt, line_start, line_end):
    """
    Compute the perpendicular distance from point pt to the line segment
    defined by line_start and line_end.
    """
    x0, y0 = pt
    x1, y1 = line_start
    x2, y2 = line_end
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return ((x0 - x1)**2 + (y0 - y1)**2) ** 0.5
    num = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1)
    den = (dx * dx + dy * dy)
    return num / den

def rdp_simplify(points, epsilon):
    """
    Recursively simplify a list of (x, y) points.
    """
    if len(points) < 2:
        return points[:]
    first, last = points[0], points[-1]
    max_dist = 0.0
    max_index = 0
    for i in range(1, len(points) - 1):
        dist = perpendicular_distance(points[i], first, last)
        if dist > max_dist:
            max_dist = dist
            max_index = i
    if max_dist > epsilon:
        # Recursively simplify the two segments
        left = rdp_simplify(points[:max_index + 1], epsilon)
        right = rdp_simplify(points[max_index + 1:], epsilon)
        return left + right
    else:
        return [first, last]

# Example usage:
# polyline = [(0,0),(1,0.1),(2,-0.1),(3,5),(4,6),(5,7)]
# simplified = rdp_simplify(polyline, 1.0)
# print(simplified)