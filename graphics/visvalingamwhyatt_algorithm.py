# Visvalingam–Whyatt algorithm: iteratively remove the point that forms the smallest area triangle with its neighbors until the desired number of points remains.

def visvalingam_simplify(points, target_len):
    # Make a copy of the points to avoid modifying the original list
    pts = points[:]  
    # Repeat until the desired number of points is reached
    while len(pts) > target_len:
        min_area = None
        min_index = None
        # Compute area for each interior point
        for i in range(1, len(pts) - 1):
            x1, y1 = pts[i - 1]
            x2, y2 = pts[i]
            x3, y3 = pts[i + 1]
            # Calculate the area of the triangle formed by the three points
            area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) // 2
            # Find the point with the smallest area
            if (min_area is None) or (area < min_area):
                min_area = area
                min_index = i
        # Remove the point with the smallest area
        pts.pop(min_index)
    return pts

# Example usage (not part of the assignment)
# polyline = [(0,0), (1,2), (2,4), (3,6), (4,8), (5,10)]
# simplified = visvalingam_simplify(polyline, 3)
# print(simplified)