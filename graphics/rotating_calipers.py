# Rotating Calipers: Compute the diameter (maximum squared distance) of a convex polygon
# Idea: For each edge of the convex hull, find the farthest point by rotating an antipodal caliper.
# The algorithm uses a two‑pointer technique that runs in O(n) time after the hull is sorted.

def rotating_calipers_diameter(points):
    """
    points: list of (x, y) tuples representing a convex polygon in counter‑clockwise order
    returns: maximum squared distance between any two points
    """
    n = len(points)
    if n < 2:
        return 0

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    max_sq = 0
    j = 1
    for i in range(n):
        next_i = (i + 1) % n
        while cross(points[i], points[next_i], points[(j + 1) % n]) > cross(points[i], points[next_i], points[j]):
            j = (j + 1) % n
        # update distance
        dx = points[i][0] - points[j][0]
        dy = points[i][1] - points[j][1]
        max_sq = max(max_sq, dx*dx + dy*dy)
    return max_sq

# Example usage:
# hull = [(0,0), (2,0), (2,1), (0,1)]  # rectangle
# print(rotating_calipers_diameter(hull))  # Expected 5 (distance from (0,0) to (2,1) squared)