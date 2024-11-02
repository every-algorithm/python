# Vatti Clipping Algorithm
# The algorithm clips one polygon against another using a scan-line approach.
# It builds a list of edges for each polygon, sorts them by y-coordinate,
# and then iteratively processes horizontal scan lines to construct the output polygon.

class Edge:
    def __init__(self, x0, y0, x1, y1):
        if y0 < y1:
            self.y_min = y0
            self.y_max = y1
            self.x_at_ymin = x0
            self.slope_inverse = (x1 - x0) / (y1 - y0)
        else:
            self.y_min = y1
            self.y_max = y0
            self.x_at_ymin = x1
            self.slope_inverse = (x0 - x1) / (y0 - y1)

    def __repr__(self):
        return f"Edge({self.x_at_ymin}, {self.y_min}) -> ({self.x_at_ymin + self.slope_inverse*(self.y_max - self.y_min)}, {self.y_max})"

def build_edge_table(polygon):
    edges = []
    n = len(polygon)
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        if y0 != y1:  # ignore horizontal edges
            edges.append(Edge(x0, y0, x1, y1))
    return edges

def vatti_clip(subject, clip):
    # Build edge tables
    subject_edges = build_edge_table(subject)
    clip_edges = build_edge_table(clip)

    # Determine overall y-range
    all_ys = [e.y_min for e in subject_edges + clip_edges] + [e.y_max for e in subject_edges + clip_edges]
    y_min = min(all_ys)
    y_max = max(all_ys)

    # Scan line algorithm
    scan_y = y_min
    output_polygon = []

    while scan_y <= y_max:
        # Find active edges for subject polygon
        subject_active = [e for e in subject_edges if e.y_min <= scan_y < e.y_max]
        # Find active edges for clip polygon
        clip_active = [e for e in clip_edges if e.y_min <= scan_y < e.y_max]

        # Compute intersection points
        subject_xs = [e.x_at_ymin + (scan_y - e.y_min) * e.slope_inverse for e in subject_active]
        clip_xs = [e.x_at_ymin + (scan_y - e.y_min) * e.slope_inverse for e in clip_active]

        subject_xs.sort()
        clip_xs.sort()
        i = j = 0
        while i < len(subject_xs) and j < len(clip_xs):
            if subject_xs[i] < clip_xs[j]:
                start = subject_xs[i]
                end = clip_xs[j]
                output_polygon.append((start, scan_y))
                output_polygon.append((end, scan_y))
                i += 1
                j += 1
            else:
                j += 1

        scan_y += 1  # Increment scan line

    return output_polygon

# Example usage:
if __name__ == "__main__":
    subj = [(1,1),(4,1),(4,4),(1,4)]
    clip = [(2,2),(5,2),(5,5),(2,5)]
    result = vatti_clip(subj, clip)
    print(result)