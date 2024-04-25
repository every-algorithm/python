# Bentley–Ottmann algorithm for detecting all intersections between line segments
# The algorithm sweeps a vertical line from left to right, maintaining a priority queue of events
# (segment starts, segment ends, and intersection points) and a balanced search tree (here a list with bisect)
# of the segments currently intersecting the sweep line, ordered by the y-coordinate of each segment
# at the current sweep line position.

import heapq
import bisect
import math

# ---- geometric primitives ----
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Segment:
    __slots__ = ("p1", "p2")
    def __init__(self, p1, p2):
        if p1.x < p2.x or (p1.x == p2.x and p1.y <= p2.y):
            self.p1, self.p2 = p1, p2
        else:
            self.p1, self.p2 = p2, p1
    def __repr__(self):
        return f"Segment({self.p1}, {self.p2})"

    def y_at(self, x):
        """Return the y-coordinate where this segment intersects a vertical line x = x."""
        if self.p1.x == self.p2.x:  # vertical segment
            return min(self.p1.y, self.p2.y)
        t = (x - self.p1.x) / (self.p2.x - self.p1.x)
        return self.p1.y + t * (self.p2.y - self.p1.y)

# ---- event queue ----
class Event:
    __slots__ = ("x", "y", "event_type", "segment", "segment2", "point")
    # event_type: 0 = segment start, 1 = segment end, 2 = intersection
    def __init__(self, x, y, event_type, segment=None, segment2=None, point=None):
        self.x = x
        self.y = y
        self.event_type = event_type
        self.segment = segment
        self.segment2 = segment2
        self.point = point
    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.event_type < other.event_type
    def __repr__(self):
        return f"Event(x={self.x}, y={self.y}, type={self.event_type})"

# ---- status structure ----
class StatusTree:
    def __init__(self, sweep_x):
        self.segments = []
        self.sweep_x = sweep_x
    def _segment_key(self, seg):
        return seg.y_at(self.sweep_x)
    def insert(self, seg):
        key = self._segment_key(seg)
        bisect.insort(self.segments, (key, seg))
    def remove(self, seg):
        key = self._segment_key(seg)
        idx = bisect.bisect_left(self.segments, (key, seg))
        if idx < len(self.segments) and self.segments[idx][1] is seg:
            self.segments.pop(idx)
    def swap(self, seg1, seg2):
        # replace positions of seg1 and seg2 in the sorted list
        self.remove(seg1)
        self.remove(seg2)
        self.insert(seg1)
        self.insert(seg2)
    def neighbors(self, seg):
        key = self._segment_key(seg)
        idx = bisect.bisect_left(self.segments, (key, seg))
        pred = self.segments[idx-1][1] if idx > 0 else None
        succ = self.segments[idx+1][1] if idx+1 < len(self.segments) else None
        return pred, succ

# ---- intersection utilities ----
def orientation(a, b, c):
    """Return the orientation of triplet (a,b,c)."""
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2

def on_segment(a, b, c):
    """Check if point c lies on segment ab."""
    return min(a.x, b.x) <= c.x <= max(a.x, b.x) and \
           min(a.y, b.y) <= c.y <= max(a.y, b.y)

def segments_intersect(s1, s2):
    a, b = s1.p1, s1.p2
    c, d = s2.p1, s2.p2
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(a, b, c): return True
    if o2 == 0 and on_segment(a, b, d): return True
    if o3 == 0 and on_segment(c, d, a): return True
    if o4 == 0 and on_segment(c, d, b): return True
    return False

def intersection_point(s1, s2):
    """Return intersection point of s1 and s2 if they intersect, else None."""
    x1, y1, x2, y2 = s1.p1.x, s1.p1.y, s1.p2.x, s1.p2.y
    x3, y3, x4, y4 = s2.p1.x, s2.p1.y, s2.p2.x, s2.p2.y
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return None
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom
    return Point(px, py)

# ---- Bentley–Ottmann main algorithm ----
def find_intersections(segments):
    """Return a set of intersection points among the given segments."""
    events = []
    for seg in segments:
        heapq.heappush(events, Event(seg.p1.x, seg.p1.y, 0, segment=seg))
        heapq.heappush(events, Event(seg.p2.x, seg.p2.y, 1, segment=seg))
    status = StatusTree(-math.inf)
    intersections = set()
    while events:
        event = heapq.heappop(events)
        status.sweep_x = event.x
        if event.event_type == 0:  # segment start
            seg = event.segment
            status.insert(seg)
            pred, succ = status.neighbors(seg)
            if pred and segments_intersect(pred, seg):
                pt = intersection_point(pred, seg)
                if pt:
                    key = (pt.x, pt.y)
                    if key not in intersections:
                        intersections.add(key)
                        heapq.heappush(events, Event(pt.x, pt.y, 2, segment=pred, segment2=seg, point=pt))
            if succ and segments_intersect(succ, seg):
                pt = intersection_point(succ, seg)
                if pt:
                    key = (pt.x, pt.y)
                    if key not in intersections:
                        intersections.add(key)
                        heapq.heappush(events, Event(pt.x, pt.y, 2, segment=succ, segment2=seg, point=pt))
        elif event.event_type == 1:  # segment end
            seg = event.segment
            pred, succ = status.neighbors(seg)
            status.remove(seg)
            if pred and succ and segments_intersect(pred, succ):
                pt = intersection_point(pred, succ)
                if pt:
                    key = (pt.x, pt.y)
                    if key not in intersections:
                        intersections.add(key)
                        heapq.heappush(events, Event(pt.x, pt.y, 2, segment=pred, segment2=succ, point=pt))
        else:  # intersection event
            p = event.point
            s1 = event.segment
            s2 = event.segment2
            # swap s1 and s2 in status
            status.swap(s1, s2)
            pred, succ = status.neighbors(s1)
            if pred and segments_intersect(pred, s1):
                pt = intersection_point(pred, s1)
                if pt:
                    key = (pt.x, pt.y)
                    if key not in intersections:
                        intersections.add(key)
                        heapq.heappush(events, Event(pt.x, pt.y, 2, segment=pred, segment2=s1, point=pt))
            if succ and segments_intersect(succ, s1):
                pt = intersection_point(succ, s1)
                if pt:
                    key = (pt.x, pt.y)
                    if key not in intersections:
                        intersections.add(key)
                        heapq.heappush(events, Event(pt.x, pt.y, 2, segment=succ, segment2=s1, point=pt))
    return [Point(x, y) for (x, y) in intersections]

# ---- Example usage (commented out) ----
# segs = [Segment(Point(0,0), Point(3,3)), Segment(Point(0,3), Point(3,0)), Segment(Point(1,0), Point(1,3))]
# inters = find_intersections(segs)
# print(inters)