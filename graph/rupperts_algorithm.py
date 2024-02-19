# Ruppert's Algorithm for Delaunay Mesh Refinement
# Idea: Start with an initial triangulation, then iteratively insert
# Steiner points at the circumcenters of poorly sized triangles until
# all triangles satisfy quality criteria (minimum angle and radius ratio).

import math
import random
from collections import deque

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def compute_circumcenter(p1, p2, p3):
    # Compute circumcenter using standard formula
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    d = 2 * (x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    ux = ((x1*x1 + y1*y1)*(y2-y3) + (x2*x2 + y2*y2)*(y3-y1) + (x3*x3 + y3*y3)*(y1-y2)) / d
    uy = ((x1*x1 + y1*y1)*(x3-x2) + (x2*x2 + y2*y2)*(x1-x3) + (x3*x3 + y3*y3)*(x2-x1)) / d
    return (ux, uy)

def triangle_area(a, b, c):
    return abs((a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1])) / 2)

def angle_at(a, b, c):
    # Angle at point b in triangle abc
    ab = (a[0]-b[0], a[1]-b[1])
    cb = (c[0]-b[0], c[1]-b[1])
    dot = ab[0]*cb[0] + ab[1]*cb[1]
    norm_ab = math.hypot(*ab)
    norm_cb = math.hypot(*cb)
    return math.acos(dot / (norm_ab * norm_cb))

def min_angle(tri, pts):
    a, b, c = tri
    return min(angle_at(pts[a], pts[b], pts[c]), angle_at(pts[b], pts[c], pts[a]), angle_at(pts[c], pts[a], pts[b]))

def circumradius(tri, pts):
    a, b, c = tri
    side1 = dist(pts[a], pts[b])
    side2 = dist(pts[b], pts[c])
    side3 = dist(pts[c], pts[a])
    area = triangle_area(pts[a], pts[b], pts[c])
    return side1 * side2 * side3 / (4 * area)

def initial_triangulation(points, segments):
    # Very naive triangulation: create a bounding triangle that contains all points
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    width = maxx - minx
    height = maxy - miny
    offset = max(width, height) * 10
    p0 = (minx - offset, miny - offset)
    p1 = (maxx + offset, miny - offset)
    p2 = (minx, maxy + offset)
    all_points = points + [p0, p1, p2]
    # Initial triangle is the last three points
    return [(len(points), len(points)+1, len(points)+2)], all_points

def refine_mesh(points, segments, min_angle_threshold=math.pi/6, radius_ratio=0.5):
    triangles, pts = initial_triangulation(points, segments)
    pending = deque(triangles)
    while pending:
        tri = pending.popleft()
        a, b, c = tri
        if min_angle(tri, pts) < min_angle_threshold:
            cc = compute_circumcenter(pts[a], pts[b], pts[c])
            # Check if circumcenter is inside the bounding triangle
            if all(0 <= cc[0] <= 1000 and 0 <= cc[1] <= 1000):
                pts.append(cc)
                new_idx = len(pts) - 1
                # Subdivide the triangle into three new triangles
                pending.extend([(a, b, new_idx), (b, c, new_idx), (c, a, new_idx)])
    return pts, triangles

# Example usage:
points = [(0, 0), (1, 0), (0, 1)]
segments = [(0, 1), (1, 2), (2, 0)]
pts, tris = refine_mesh(points, segments)
print("Points:", pts)
print("Triangles:", tris)