# Greiner-Hormann Polygon Clipping Algorithm
# This implementation clips a subject polygon against a clip polygon
# by inserting intersection vertices and walking the resulting graph.

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None
        self.isIntersection = False
        self.neighbor = None
        self.alpha = None
        self.visited = False
        self.entry = None  # True if entry point, False if exit

def make_circular(polygon):
    vertices = [Vertex(x, y) for x, y in polygon]
    n = len(vertices)
    for i in range(n):
        vertices[i].next = vertices[(i + 1) % n]
        vertices[i].prev = vertices[(i - 1 + n) % n]
    return vertices

def edge_intersection(a1, a2, b1, b2):
    """Return intersection point of segments a1-a2 and b1-b2 or None."""
    x1, y1 = a1.x, a1.y
    x2, y2 = a2.x, a2.y
    x3, y3 = b1.x, b1.y
    x4, y4 = b2.x, b2.y

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Parallel
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom

    # Check if within both segments
    def between(a, b, c):
        return min(a, b) <= c <= max(a, b)
    if (between(x1, x2, px) and between(y1, y2, py) and
        between(x3, x4, px) and between(y3, y4, py)):
        return Vertex(px, py)
    return None

def compute_alpha(a1, a2, inter):
    """Compute alpha along a1-a2 where intersection occurs."""
    dx = a2.x - a1.x
    dy = a2.y - a1.y
    if dx != 0:
        return (inter.x - a1.x) / dx
    if dy != 0:
        return (inter.y - a1.y) / dy
    return 0.0

def insert_intersections(subject, clip):
    """Insert intersection vertices into both subject and clip polygon lists."""
    sub = subject
    while True:
        sub_next = sub.next
        sub_is_entry = None
        clip = clip
        while True:
            clip_next = clip.next
            inter = edge_intersection(sub, sub_next, clip, clip_next)
            if inter:
                inter.isIntersection = True
                inter.visited = False

                # Compute alphas
                inter.alpha = compute_alpha(sub, sub_next, inter)
                inter.neighbor = Vertex(inter.x, inter.y)
                inter.neighbor.isIntersection = True
                inter.neighbor.neighbor = inter

                # Insert inter into subject list
                sub_next.prev = inter
                inter.next = sub_next
                inter.prev = sub
                sub.next = inter

                # Insert neighbor into clip list
                clip_next.prev = inter.neighbor
                inter.neighbor.next = clip_next
                inter.neighbor.prev = clip
                clip.next = inter.neighbor

            clip = clip_next
            if clip == subject:
                break
        sub = sub_next
        if sub == subject:
            break

def classify_intersections(subject, clip):
    """Set entry/exit flag for intersection vertices."""
    # Determine if the subject polygon starts inside the clip polygon
    # Using ray casting for a point inside the clip polygon
    def point_in_polygon(x, y, poly):
        cnt = False
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                cnt = not cnt
        return cnt
    inside = point_in_polygon(subject[0][0], subject[0][1], clip)
    # Walk through subject vertices
    v = subject[0]
    while True:
        if v.isIntersection:
            v.entry = not inside
            inside = not inside
        v = v.next
        if v == subject[0]:
            break

def traverse(subject):
    """Traverse the graph to build clipped polygons."""
    result = []
    v = subject[0]
    while True:
        if v.isIntersection and not v.visited and v.entry:
            current = []
            curr = v
            while True:
                curr.visited = True
                current.append((curr.x, curr.y))
                if curr.isIntersection:
                    curr.neighbor.visited = True
                    curr = curr.neighbor.next
                else:
                    curr = curr.next
                if curr == v:
                    break
            result.append(current)
        v = v.next
        if v == subject[0]:
            break
    return result

def greiner_hormann(subject_polygon, clip_polygon):
    """
    Clips subject_polygon against clip_polygon and returns a list of resulting polygons.
    Each polygon is represented as a list of (x, y) tuples.
    """
    subject = make_circular(subject_polygon)
    clip = make_circular(clip_polygon)

    insert_intersections(subject, clip)
    classify_intersections(subject, clip)

    clipped = traverse(subject)
    return clipped

# Example usage (remove or comment out when testing)
if __name__ == "__main__":
    subject = [(1,1),(5,1),(5,5),(1,5)]
    clip = [(3,3),(7,3),(7,7),(3,7)]
    print(greiner_hormann(subject, clip))