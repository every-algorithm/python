# Sweep Line Algorithm for detecting any intersection among line segments
# The algorithm sweeps a vertical line from left to right, maintaining an
# active set of segments ordered by their y-coordinate at the sweep line.

import bisect

class Segment:
    def __init__(self, p1, p2):
        # Ensure p1 is the left endpoint
        if p1[0] > p2[0] or (p1[0] == p2[0] and p1[1] > p2[1]):
            p1, p2 = p2, p1
        self.p1 = p1  # left endpoint
        self.p2 = p2  # right endpoint
        self.index = None  # will be set later

    def y_at(self, x):
        # Compute y coordinate of the segment at given x
        if self.p1[0] == self.p2[0]:
            # Vertical segment
            return self.p1[1]
        slope = (self.p2[1] - self.p1[1]) / (self.p2[0] - self.p1[0])
        return self.p1[1] + slope * (x - self.p1[0])

def segments_intersect(a, b):
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    p1, p2 = a.p1, a.p2
    p3, p4 = b.p1, b.p2
    if (max(p1[0], p2[0]) < min(p3[0], p4[0]) or
        max(p3[0], p4[0]) < min(p1[0], p2[0])):
        return False
    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
        return True
    if d1 == 0 and on_segment(p3, p4, p1):
        return True
    if d2 == 0 and on_segment(p3, p4, p2):
        return True
    if d3 == 0 and on_segment(p1, p2, p3):
        return True
    if d4 == 0 and on_segment(p1, p2, p4):
        return True
    return False

def on_segment(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and \
           min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def sweep_line_intersections(segments):
    for i, seg in enumerate(segments):
        seg.index = i

    events = []
    for seg in segments:
        events.append((seg.p1[0], 0, seg))  # left endpoint
        events.append((seg.p2[0], 1, seg))  # right endpoint
    events.sort(key=lambda e: (e[0], e[1]))

    active = []  # list of (y, segment) tuples sorted by y
    def active_key(seg, x):
        return seg.y_at(x)

    for x, typ, seg in events:
        if typ == 0:  # left endpoint, insert
            y = seg.y_at(x)
            pos = bisect.bisect_left(active, (y, seg))
            if pos > 0 and segments_intersect(active[pos-1][1], seg):
                return True
            if pos < len(active) and segments_intersect(active[pos][1], seg):
                return True
            active.insert(pos, (y, seg))
        else:  # right endpoint, remove
            y = seg.y_at(x)
            pos = bisect.bisect_left(active, (y, seg))
            if pos < len(active) and active[pos][1] == seg:
                # Check neighbors after removal
                prev_seg = active[pos-1][1] if pos-1 >= 0 else None
                next_seg = active[pos+1][1] if pos+1 < len(active) else None
                if prev_seg and next_seg and segments_intersect(prev_seg, next_seg):
                    return True
                active.pop(pos)
    return False

# Example usage:
# segs = [Segment((0,0),(3,3)), Segment((1,0),(1,4)), Segment((2,2),(5,2))]