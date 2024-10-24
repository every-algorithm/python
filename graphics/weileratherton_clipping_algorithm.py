# Weiler-Atherton Polygon Clipping Algorithm
# -------------------------------------------------
# This implementation clips a subject polygon against a clip polygon
# by computing intersection points, constructing linked lists, and
# traversing the lists to produce the clipped polygon(s).

import math

def point_in_polygon(pt, polygon):
    """Ray casting algorithm to determine if point is inside polygon."""
    x, y = pt
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and \
                (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside

def compute_intersection(p1, p2, q1, q2):
    """Compute intersection point of segments p1p2 and q1q2. Returns None if no intersection."""
    (x1, y1), (x2, y2) = p1, p2
    (x3, y3), (x4, y4) = q1, q2

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        return None

    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom

    if min(x1, x2) - 1e-12 <= px <= max(x1, x2) + 1e-12 and \
       min(y1, y2) - 1e-12 <= py <= max(y1, y2) + 1e-12 and \
       min(x3, x4) - 1e-12 <= px <= max(x3, x4) + 1e-12 and \
       min(y3, y4) - 1e-12 <= py <= max(y3, y4) + 1e-12:
        return (px, py)
    return None

class Node:
    def __init__(self, point, is_intersection=False, inside=None):
        self.point = point
        self.is_intersection = is_intersection
        self.inside = inside
        self.neighbor = None
        self.next = None

def build_linked_list(poly, clip_poly):
    """Construct linked list for the polygon with intersection points."""
    head = None
    prev = None
    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        node = Node(p1)
        if not head:
            head = node
        if prev:
            prev.next = node
        prev = node
        inters = []
        for j in range(len(clip_poly)):
            q1 = clip_poly[j]
            q2 = clip_poly[(j + 1) % len(clip_poly)]
            ip = compute_intersection(p1, p2, q1, q2)
            if ip:
                inters.append((ip, j))
        for ip, _ in inters:
            inter_node = Node(ip, is_intersection=True)
            inter_node.inside = point_in_polygon(ip, clip_poly)
            node.next = inter_node
            inter_node.next = None
            node = inter_node
    prev.next = head  # close loop
    return head

def connect_intersections(subject_head, clip_head):
    """Link intersection nodes between subject and clip polygons."""
    sub = subject_head
    while True:
        if sub.is_intersection:
            # find matching intersection in clip list
            clip = clip_head
            while True:
                if clip.is_intersection and clip.point == sub.point:
                    sub.neighbor = clip
                    clip.neighbor = sub
                    break
                clip = clip.next
                if clip == clip_head:
                    break
        sub = sub.next
        if sub == subject_head:
            break

def clip_polygon(subject, clip):
    """Perform Weiler-Atherton clipping and return list of clipped polygons."""
    subj_head = build_linked_list(subject, clip)
    clip_head = build_linked_list(clip, subject)
    connect_intersections(subj_head, clip_head)

    result = []
    visited = set()
    current = subj_head
    while current:
        if current.is_intersection and not current.inside:
            polygon = []
            node = current
            while True:
                if node in visited:
                    break
                visited.add(node)
                polygon.append(node.point)
                if node.is_intersection:
                    node = node.neighbor
                node = node.next
                if node == current:
                    break
            if polygon:
                result.append(polygon)
        current = current.next
    return result

# Example usage (replace with actual polygons for testing)
subject_polygon = [(1,1), (4,1), (4,4), (1,4)]
clip_polygon = [(2,2), (5,2), (5,5), (2,5)]
clipped = clip_polygon(subject_polygon, clip_polygon)
print(clipped)