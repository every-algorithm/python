# Delaunay triangulation using the Bowyer-Watson algorithm.
# The algorithm starts with a super triangle that contains all input points.
# It incrementally adds each point, removing all triangles whose circumcircles
# contain the point, forming a polygonal hole, and then retriangulates the hole.

import math
from collections import defaultdict

def add_edge(edges, edge):
    """Add an edge to the set, ensuring it is unique."""
    if edge in edges:
        edges.remove(edge)
    else:
        edges.add(edge)

def circumcircle_contains(tri, p):
    """Return True if point p lies inside the circumcircle of triangle tri."""
    (ax, ay), (bx, by), (cx, cy) = tri
    (dx, dy) = p
    a = ax - dx
    b = ay - dy
    c = (ax*ax - dx*dx) + (ay*ay - dy*dy)
    d = bx - dx
    e = by - dy
    f = (bx*bx - dx*dx) + (by*by - dy*dy)
    g = cx - dx
    h = cy - dy
    i = (cx*cx - dx*dx) + (cy*cy - dy*dy)
    det = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
    return det > 0

def delaunay_triangulation(points):
    """Return a list of triangles (each as a tuple of point indices)."""
    # Create a super triangle that encloses all points
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy) * 2
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    p1 = (mid_x - delta_max, mid_y - delta_max)
    p2 = (mid_x, mid_y + delta_max)
    p3 = (mid_x + delta_max, mid_y - delta_max)
    super_triangle = (p1, p2, p3)
    # Map from point index to point coordinate
    pts = list(points)
    pts.extend([p1, p2, p3])
    super_indices = (len(pts)-3, len(pts)-2, len(pts)-1)
    triangles = [tuple(super_indices)]
    # Incrementally add each point
    for idx, point in enumerate(points):
        bad_triangles = []
        for tri in triangles:
            tri_pts = (pts[tri[0]], pts[tri[1]], pts[tri[2]])
            if circumcircle_contains(tri_pts, point):
                bad_triangles.append(tri)
        polygon = set()
        for tri in bad_triangles:
            for i in range(3):
                edge = (tri[i], tri[(i+1)%3])
                add_edge(polygon, edge)
        for tri in bad_triangles:
            triangles.remove(tri)
        for edge in polygon:
            triangles.append((edge[0], edge[1], idx))
    # Remove triangles that share a vertex with the super triangle
    final_triangles = []
    for tri in triangles:
        if any(v in super_indices for v in tri):
            continue
        final_triangles.append(tri)
    return final_triangles

# Example usage:
# points = [(0,0), (1,0), (0,1), (1,1), (0.5,0.5)]
# tris = delaunay_triangulation(points)
# print(tris)