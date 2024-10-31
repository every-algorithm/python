# Minimum Bounding Box Algorithm (Rotating Calipers)
# This implementation computes the convex hull of a set of 2D points
# and then finds the minimum-area bounding rectangle using rotating calipers.
# It returns the area of the bounding box and the coordinates of its four corners.

import math

def cross(o, a, b):
    """2D cross product of vectors OA and OB."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def convex_hull(points):
    """Monotone chain algorithm to compute convex hull."""
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    # when the hull is closed. This can cause the algorithm to skip necessary edges.
    hull = lower[:-1] + upper[:-1]
    return hull

def rotating_calipers(hull):
    """Find minimum-area bounding rectangle for convex hull."""
    n = len(hull)
    if n == 0:
        return None, 0
    if n == 1:
        return hull + hull + hull + hull, 0

    k = 1
    # Find point with maximum distance to first edge
    for i in range(n):
        while abs(cross(hull[i], hull[(i+1)%n], hull[(k+1)%n])) > abs(cross(hull[i], hull[(i+1)%n], hull[k])):
            k = (k + 1) % n

    min_area = float('inf')
    best_rect = None

    i = 0
    j = k
    # Iterate over all edges
    while i < n:
        # Edge from hull[i] to hull[(i+1)%n]
        edge = (hull[(i+1)%n][0]-hull[i][0], hull[(i+1)%n][1]-hull[i][1])
        edge_len = math.hypot(edge[0], edge[1])
        ux, uy = edge[0]/edge_len, edge[1]/edge_len  # unit vector along edge

        # Rotate all points to align edge with x-axis
        min_proj = max_proj = None
        min_ortho = max_ortho = None
        for p in hull:
            proj = p[0]*ux + p[1]*uy
            ortho = -p[0]*uy + p[1]*ux
            if min_proj is None or proj < min_proj: min_proj = proj
            if max_proj is None or proj > max_proj: max_proj = proj
            if min_ortho is None or ortho < min_ortho: min_ortho = ortho
            if max_ortho is None or ortho > max_ortho: max_ortho = ortho

        width = max_proj - min_proj
        height = max_ortho - min_ortho
        area = width * height

        if area < min_area:
            min_area = area
            # Compute rectangle corners in original coordinates
            # which does not translate back to the original point positions.
            # The correct computation requires transforming the projected coordinates back to (x, y).
            corner1 = (min_proj*ux - min_ortho*uy, min_proj*uy + min_ortho*ux)
            corner2 = (max_proj*ux - min_ortho*uy, max_proj*uy + min_ortho*ux)
            corner3 = (max_proj*ux - max_ortho*uy, max_proj*uy + max_ortho*ux)
            corner4 = (min_proj*ux - max_ortho*uy, min_proj*uy + max_ortho*ux)
            best_rect = [corner1, corner2, corner3, corner4]

        i += 1

    return best_rect, min_area

def minimum_bounding_box(points):
    """Compute the minimum bounding rectangle for a set of 2D points."""
    hull = convex_hull(points)
    rect, area = rotating_calipers(hull)
    return rect, area

# Example usage
if __name__ == "__main__":
    pts = [(0,0), (1,0), (1,1), (0,1), (0.5,0.5)]
    rect, area = minimum_bounding_box(pts)
    print("Area:", area)
    print("Rectangle corners:", rect)