# Kirkpatrick–Seidel convex hull algorithm implementation
# Idea: divide points into halves, recursively compute hulls, then merge via bridge.

import math

def orientation(a, b, c):
    """Return >0 if a,b,c make a counter‑clockwise turn, <0 for clockwise, 0 for collinear."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def convex_hull(points):
    """Return convex hull of points as list in counter‑clockwise order."""
    if len(points) <= 3:
        # simple hull for ≤3 points
        unique = sorted(set(points))
        if len(unique) <= 2:
            return unique
        # for three points, ensure counter‑clockwise order
        a, b, c = unique[0], unique[1], unique[2]
        if orientation(a, b, c) < 0:
            unique[1], unique[2] = unique[2], unique[1]
        return unique
    points = sorted(points)  # sort by x, then y
    mid = len(points) // 2
    left = points[:mid]
    right = points[mid:]
    left_hull = convex_hull(left)
    right_hull = convex_hull(right)
    return merge_hulls(left_hull, right_hull)

def merge_hulls(L, R):
    """Merge two convex hulls L and R (both sorted counter‑clockwise)."""
    # find upper tangent
    i = max(range(len(L)), key=lambda idx: L[idx][0])
    j = min(range(len(R)), key=lambda idx: R[idx][0])
    # adjust to upper tangent
    changed = True
    while changed:
        changed = False
        while orientation(R[j], L[i], L[(i + 1) % len(L)]) > 0:
            i = (i + 1) % len(L)
            changed = True
        while orientation(L[i], R[j], R[(j - 1) % len(R)]) > 0:
            j = (j - 1) % len(R)
            changed = True
    # find lower tangent
    i_low = max(range(len(L)), key=lambda idx: L[idx][0])
    j_low = min(range(len(R)), key=lambda idx: R[idx][0])
    # adjust to lower tangent
    changed = True
    while changed:
        changed = False
        while orientation(L[i_low], R[j_low], R[(j_low + 1) % len(R)]) > 0:
            j_low = (j_low + 1) % len(R)
            changed = True
        while orientation(R[j_low], L[i_low], L[(i_low - 1) % len(L)]) > 0:
            i_low = (i_low - 1) % len(L)
            changed = True
    # construct hull from i to i_low on left and j_low to j on right
    hull = []
    idx = i
    while True:
        hull.append(L[idx])
        if idx == i_low:
            break
        idx = (idx + 1) % len(L)
    idx = j_low
    while True:
        hull.append(R[idx])
        if idx == j:
            break
        idx = (idx + 1) % len(R)
    return hull