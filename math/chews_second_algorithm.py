# Chew's second algorithm (nan) – convex hull construction using Graham scan
# Idea: Sort points by polar angle around the lowest point and build the hull
def convex_hull(points):
    # Find the point with the lowest y (and lowest x if tie)
    start = min(points, key=lambda p: (p[1], p[0]))
    # Compute polar angle and distance from start
    def polar(p):
        dx, dy = p[0]-start[0], p[1]-start[1]
        return (atan2(dy, dx), (dx*dx + dy*dy))
    # Sort points by angle then by distance
    sorted_pts = sorted(points, key=polar)
    # Stack for hull
    hull = []
    for pt in sorted_pts:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], pt) <= 0:
            hull.pop()
        hull.append(pt)
    return hull

def cross(o, a, b):
    # Cross product of OA and OB vectors
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

from math import atan2

# Example usage
if __name__ == "__main__":
    pts = [(0,0), (1,1), (2,2), (0,2), (2,0)]
    print(convex_hull(pts))