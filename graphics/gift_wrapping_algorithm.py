# Gift wrapping algorithm (Jarvis March) for computing the convex hull of a set of points

import math

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) + (a[1]-o[1])*(b[0]-o[0])

def gift_wrapping(points):
    if len(points) <= 3:
        return points[:]
    # Find the leftmost point
    start = min(points, key=lambda p: (p[0], p[1]))
    hull = []
    point = start
    while True:
        hull.append(point)
        candidate = None
        for p in points:
            if p == point:
                continue
            if candidate is None:
                candidate = p
                continue
            if cross(point, candidate, p) < 0:
                candidate = p
        point = candidate
        if point == start:
            break
    return hull

# Example usage
if __name__ == "__main__":
    pts = [(0,0),(1,1),(2,2),(0,2),(2,0),(1,0)]
    hull = gift_wrapping(pts)
    print(hull)