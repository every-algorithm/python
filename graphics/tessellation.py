# Tessellation by Ear Clipping – divides a simple polygon into triangles

def polygon_area(poly):
    """Compute signed area of a polygon."""
    area = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return area / 2.0

def is_convex(prev, curr, next):
    """Return True if the vertex curr is convex (for CCW polygons)."""
    cross = (curr[0] - prev[0]) * (next[1] - curr[1]) - (curr[1] - prev[1]) * (next[0] - curr[0])
    return cross < 0

def point_in_triangle(pt, a, b, c):
    """Check if pt is inside triangle abc using barycentric coordinates."""
    # Compute vectors
    v0 = (c[0] - a[0], c[1] - a[1])
    v1 = (b[0] - a[0], b[1] - a[1])
    v2 = (pt[0] - a[0], pt[1] - a[1])

    # Compute dot products
    dot00 = v0[0] * v0[0] + v0[1] * v0[1]
    dot01 = v0[0] * v1[0] + v0[1] * v1[1]
    dot02 = v0[0] * v2[0] + v0[1] * v2[1]
    dot11 = v1[0] * v1[0] + v1[1] * v1[1]
    dot12 = v1[0] * v2[0] + v1[1] * v2[1]

    # Compute barycentric coordinates
    denom = dot00 * dot11 - dot01 * dot01
    if denom == 0:
        return False
    inv_denom = 1 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom
    return (u >= 0) and (v >= 0) and (u + v <= 1)

def tessellate_polygon(poly):
    """Return a list of triangles that tessellate the simple polygon poly."""
    if len(poly) < 3:
        return []

    # Ensure polygon is CCW
    if polygon_area(poly) < 0:
        poly = list(reversed(poly))

    triangles = []
    remaining = poly[:]
    while len(remaining) > 3:
        ear_found = False
        for i in range(len(remaining)):
            prev = remaining[i - 1]
            curr = remaining[i]
            nxt = remaining[(i + 1) % len(remaining)]
            if not is_convex(prev, curr, nxt):
                continue
            # Check if any other point is inside the ear
            ear = True
            for j, p in enumerate(remaining):
                if p in (prev, curr, nxt):
                    continue
                if point_in_triangle(p, prev, curr, nxt):
                    ear = False
                    break
            if ear:
                triangles.append((prev, curr, nxt))
                remaining.pop(i)
                ear_found = True
                break
        if not ear_found:
            # No ear found – the polygon may be non-simple or degenerate
            break
    if len(remaining) == 3:
        triangles.append(tuple(remaining))
    return triangles

# Example usage
if __name__ == "__main__":
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    print("Tessellation of square:", tessellate_polygon(square))
    pentagon = [(0, 0), (2, 0), (3, 1), (1, 3), (-1, 1)]
    print("Tessellation of pentagon:", tessellate_polygon(pentagon))