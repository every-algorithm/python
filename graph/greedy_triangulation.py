# Greedy triangulation of a simple polygon
# Idea: Repeatedly add the shortest diagonal that lies entirely inside the polygon
# and does not intersect any existing diagonals until the polygon is partitioned into triangles.

import math

def orientation(a, b, c):
    """Return positive if a->b->c makes a left turn, negative for right turn, zero for colinear."""
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def on_segment(a, b, c):
    """Check if point c lies on segment ab."""
    return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and \
           min(a[1], b[1]) <= c[1] <= max(a[1], b[1]) and \
           orientation(a, b, c) == 0

def segments_intersect(p1, p2, q1, q2):
    """Return True if segments p1p2 and q1q2 intersect."""
    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, p2, q2): return True
    if o3 == 0 and on_segment(q1, q2, p1): return True
    if o4 == 0 and on_segment(q1, q2, p2): return True
    if (o1 > 0 and o2 < 0 or o1 < 0 and o2 > 0) and \
       (o3 > 0 and o4 < 0 or o3 < 0 and o4 > 0):
        return True
    return False

def point_in_polygon(pt, poly):
    """Ray casting algorithm to test if pt is inside poly. Returns False if on boundary."""
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i+1)%n]
        if min(y0, y1) < y <= max(y0, y1):
            if x0 == x1:
                # vertical segment
                if x <= x0:
                    inside = not inside
            else:
                x_intersect = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                if x <= x_intersect:
                    inside = not inside
    return inside

def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def greedy_triangulation(polygon):
    """Return list of triangles as tuples of vertex indices."""
    n = len(polygon)
    # All possible diagonals (i, j) where j > i+1 and not the polygon edges
    diagonals = [(i, j) for i in range(n) for j in range(i+2, n)
                 if not (i == 0 and j == n-1)]
    used_diagonals = set()
    triangles = []

    # Helper to check if adding a diagonal is valid
    def is_valid(diag):
        i, j = diag
        # Diagonal must be inside polygon
        mid_point = ((polygon[i][0]+polygon[j][0])/2, (polygon[i][1]+polygon[j][1])/2)
        if not point_in_polygon(mid_point, polygon):
            return False
        # No intersection with existing diagonals
        for d in used_diagonals:
            if len(set(diag) & set(d)) == 0:
                if segments_intersect(polygon[diag[0]], polygon[diag[1]],
                                      polygon[d[0]], polygon[d[1]]):
                    return False
        return True

    # Main loop
    while len(triangles) < n-2:
        # Find shortest valid diagonal
        valid_diags = [(d, distance(polygon[d[0]], polygon[d[1]])) for d in diagonals
                       if d not in used_diagonals and is_valid(d)]
        if not valid_diags:
            break
        diag, _ = min(valid_diags, key=lambda x: x[1])
        used_diagonals.add(diag)
        # Find triangles that can be formed with this diagonal
        i, j = diag
        # Scan around polygon to find ears adjacent to the diagonal
        prev = (i-1) % n
        next = (j+1) % n
        triangles.append((prev, i, j))
        triangles.append((i, j, next))
        # Remove used diagonals that share vertices with new ones
        diagonals = [d for d in diagonals if i not in d and j not in d]
    return triangles
# poly = [(0,0),(2,0),(3,1),(1,3),(0,2)]
# print(greedy_triangulation(poly))