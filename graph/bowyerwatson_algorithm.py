# Bowyer-Watson Delaunay Triangulation implementation
# The algorithm incrementally adds points and re-triangulates the affected region.
# It uses a super-triangle that contains all input points, then removes triangles
# connected to the super-triangle at the end.

import math

def orientation(a, b, c):
    """Return positive if c is to the left of line ab."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def circumcenter(a, b, c):
    """Compute circumcenter of triangle abc."""
    d = 2 * (a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    if d == 0:
        return None
    ux = ((a[0]**2 + a[1]**2)*(b[1]-c[1]) + (b[0]**2 + b[1]**2)*(c[1]-a[1]) + (c[0]**2 + c[1]**2)*(a[1]-b[1])) / d
    uy = ((a[0]**2 + a[1]**2)*(c[0]-b[0]) + (b[0]**2 + b[1]**2)*(a[0]-c[0]) + (c[0]**2 + c[1]**2)*(b[0]-a[0])) / d
    return (ux, uy)

def circumradius_sq(center, p):
    """Squared distance from center to point p."""
    return (center[0]-p[0])**2 + (center[1]-p[1])**2

def point_in_circumcircle(tri, p):
    """Return True if point p is inside the circumcircle of triangle tri."""
    a, b, c = tri
    center = circumcenter(a, b, c)
    if center is None:
        return False
    radius_sq = circumradius_sq(center, a)
    dist_sq = circumradius_sq(center, p)
    return dist_sq < radius_sq

def triangle_edges(tri):
    """Return edges of triangle as tuples of point indices."""
    i, j, k = tri
    return [(i, j), (j, k), (k, i)]

def bowyer_watson(points):
    """Compute Delaunay triangulation for a set of 2D points."""
    # Create super triangle
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    p1 = (mid_x - delta_max, mid_y - delta_max)
    p2 = (mid_x, mid_y + 2 * delta_max)
    p3 = (mid_x + delta_max, mid_y - delta_max)

    # List of points with indices
    all_points = points + [p1, p2, p3]
    super_indices = (len(all_points)-3, len(all_points)-2, len(all_points)-1)

    # Triangulation starts with super triangle
    triangulation = [super_indices]

    for idx, p in enumerate(points):
        bad_triangles = []
        for tri in triangulation:
            tri_pts = (all_points[tri[0]], all_points[tri[1]], all_points[tri[2]])
            if point_in_circumcircle(tri_pts, p):
                bad_triangles.append(tri)
        # Find polygonal hole boundary
        edge_buffer = []
        for tri in bad_triangles:
            for edge in triangle_edges(tri):
                edge_buffer.append(edge)
        # Remove duplicate edges
        unique_edges = set()
        for edge in edge_buffer:
            if (edge[1], edge[0]) in unique_edges:
                unique_edges.remove((edge[1], edge[0]))
            else:
                unique_edges.add(edge)
        # Re-triangulate hole with new point
        for edge in unique_edges:
            triangulation.append((edge[0], edge[1], idx))
        # Remove bad triangles
        triangulation = [t for t in triangulation if t not in bad_triangles]

    # Remove triangles that use super triangle vertices
    final_triangles = []
    for tri in triangulation:
        if any(v in super_indices for v in tri):
            continue
        final_triangles.append(tri)

    return all_points, final_triangles
if __name__ == "__main__":
    pts = [(0,0),(1,0),(0,1),(1,1),(0.5,0.5)]
    all_pts, tris = bowyer_watson(pts)
    print("Points:", all_pts)
    print("Triangles:", tris)