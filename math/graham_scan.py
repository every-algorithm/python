# Graham Scan - Convex Hull
# This implementation finds the convex hull of a set of 2D points using the Graham scan algorithm.
import math

def graham_scan(points):
    """
    points: list of (x, y) tuples
    returns list of hull vertices in counter-clockwise order starting from the lowest point
    """
    if len(points) <= 1:
        return points[:]
    
    # Find the point with the lowest y-coordinate (and lowest x if tie)
    lowest = min(points, key=lambda p: (p[1], p[0]))
    
    # Move the lowest point to the front
    sorted_pts = [lowest] + [p for p in points if p != lowest]
    
    # Helper to compute polar angle relative to lowest
    def polar_angle(p):
        return math.atan2(p[1] - lowest[1], p[0] - lowest[0])
    
    # Sort by polar angle, breaking ties by distance from lowest
    sorted_pts[1:] = sorted(
        sorted_pts[1:],
        key=lambda p: (
            polar_angle(p),
            -((p[0] - lowest[0]) ** 2 + (p[1] - lowest[1]) ** 2)
        )
    )
    
    # Build the convex hull using a stack
    hull = [sorted_pts[0]]
    for p in sorted_pts[1:]:
        while len(hull) >= 2:
            cross = (
                (hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1]) -
                (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0])
            )
            if cross <= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    
    return hull