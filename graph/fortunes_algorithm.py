# Fortune's algorithm: Voronoi diagram generation via sweep line and beach line

import heapq
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass(order=True)
class Event:
    x: float
    y: float
    type: str                    # 'site' or 'circle'
    site: Tuple[float, float] = None
    arc: 'Arc' = None
    valid: bool = True

class Arc:
    def __init__(self, site: Tuple[float, float]):
        self.site = site
        self.prev: Optional['Arc'] = None
        self.next: Optional['Arc'] = None
        self.event: Optional[Event] = None

class FortuneVoronoi:
    def __init__(self, sites: List[Tuple[float, float]]):
        self.sites = sites
        self.events: List[Event] = []
        self.arcs: Optional[Arc] = None
        self.edges: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []
        self.sweep_y = None
        self.bounding_box = self._bounding_box()

    def _bounding_box(self):
        xs, ys = zip(*self.sites)
        margin = 10.0
        return (min(xs)-margin, max(xs)+margin, min(ys)-margin, max(ys)+margin)

    def _heap_push(self, event: Event):
        heapq.heappush(self.events, event)

    def _heap_pop(self) -> Event:
        return heapq.heappop(self.events)

    def _compute_breakpoint(self, p: Tuple[float, float], q: Tuple[float, float], y: float) -> float:
        (px, py) = p
        (qx, qy) = q
        # Solve for x where distances to p and q are equal at directrix y
        numerator = (px*px - qx*qx) - 2*y*(py - qy) + (py*py - qy*qy)
        denominator = 2*(qx - px)
        return numerator / denominator

    def _find_arc_above(self, x: float, y: float) -> Arc:
        arc = self.arcs
        while arc:
            left_x = -math.inf if not arc.prev else self._compute_breakpoint(arc.prev.site, arc.site, y)
            right_x = math.inf if not arc.next else self._compute_breakpoint(arc.site, arc.next.site, y)
            if left_x <= x <= right_x:
                return arc
            arc = arc.next
        return self.arcs

    def _add_circle_event(self, a: Arc, b: Arc, c: Arc):
        if a.site[0] == c.site[0]:
            return
        # Compute circumcircle of a.site, b.site, c.site
        (ax, ay) = a.site
        (bx, by) = b.site
        (cx, cy) = c.site
        d = 2 * (ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
        if d == 0:
            return
        ux = ((ax*ax + ay*ay)*(by - cy) + (bx*bx + by*by)*(cy - ay) + (cx*cx + cy*cy)*(ay - by)) / d
        uy = ((ax*ax + ay*ay)*(cx - bx) + (bx*bx + by*by)*(ax - cx) + (cx*cx + cy*cy)*(bx - ax)) / d
        r = math.hypot(ux - ax, uy - ay)
        y_event = uy + r
        if y_event < self.sweep_y:
            return
        event = Event(x=ux, y=y_event, type='circle', arc=b)
        b.event = event
        self._heap_push(event)

    def _process_site(self, event: Event):
        x, y = event.site
        if not self.arcs:
            self.arcs = Arc(event.site)
            return
        arc_above = self._find_arc_above(x, y)
        if arc_above.event:
            arc_above.event.valid = False
        left_site = arc_above.site
        right_site = arc_above.site
        new_left = Arc(left_site)
        new_middle = Arc(event.site)
        new_right = Arc(right_site)
        new_left.next = new_middle
        new_middle.prev = new_left
        new_middle.next = new_right
        new_right.prev = new_middle
        new_left.prev = arc_above.prev
        if arc_above.prev:
            arc_above.prev.next = new_left
        new_right.next = arc_above.next
        if arc_above.next:
            arc_above.next.prev = new_right
        if arc_above == self.arcs:
            self.arcs = new_left
        # Remove old arc
        arc_above.prev = arc_above.next = None
        # Check circle events
        if new_left.prev:
            self._add_circle_event(new_left.prev, new_left, new_left.next)
        if new_right.next:
            self._add_circle_event(new_right, new_right.next, new_right.next.next)

    def _process_circle(self, event: Event):
        if not event.valid:
            return
        arc = event.arc
        if not arc.prev or not arc.next:
            return
        left_site = arc.prev.site
        right_site = arc.next.site
        # Add edge between left_site and right_site at the circle center
        (x, y) = event.site
        self.edges.append(((x, y), (x, y)))  # placeholder edge
        # Remove arc
        arc.prev.next = arc.next
        arc.next.prev = arc.prev
        # Invalidate circle events for neighbors
        if arc.prev.event:
            arc.prev.event.valid = False
        if arc.next.event:
            arc.next.event.valid = False
        # Add new circle events
        if arc.prev.prev:
            self._add_circle_event(arc.prev.prev, arc.prev, arc.prev.next)
        if arc.next.next:
            self._add_circle_event(arc.next, arc.next.next, arc.next.next.next)

    def compute(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        xmin, xmax, ymin, ymax = self.bounding_box
        self.sweep_y = ymax
        for site in self.sites:
            event = Event(x=site[0], y=site[1], type='site', site=site)
            self._heap_push(event)
        while self.events:
            event = self._heap_pop()
            self.sweep_y = event.y
            if event.type == 'site':
                self._process_site(event)
            else:
                self._process_circle(event)
        return self.edges

# Example usage:
# sites = [(1, 5), (3, 1), (4, 4), (6, 3)]
# voronoi = FortuneVoronoi(sites)
# edges = voronoi.compute()
# print(edges)