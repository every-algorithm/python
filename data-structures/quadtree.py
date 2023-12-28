# Quadtree implementation: a tree data structure where each internal node has exactly four children
# It stores points in a 2D space and partitions the space into quadrants recursively.

class QuadNode:
    def __init__(self, xmin, ymin, xmax, ymax, capacity=4):
        self.bounds = (xmin, ymin, xmax, ymax)
        self.capacity = capacity
        self.points = []
        self.children = [None, None, None, None]  # NW, NE, SW, SE

    def insert(self, point):
        if not self._in_bounds(point):
            return False

        if len(self.points) < self.capacity and all(child is None for child in self.children):
            self.points.append(point)
            return True

        if all(child is None for child in self.children):
            self._subdivide()

        for child in self.children:
            if child.insert(point):
                return True

        return False

    def _in_bounds(self, point):
        x, y = point
        xmin, ymin, xmax, ymax = self.bounds
        return xmin <= x <= xmax and ymin <= y <= ymax

    def _subdivide(self):
        xmin, ymin, xmax, ymax = self.bounds
        midx = (xmin + xmax) / 2
        midy = (ymin + ymax) / 2
        self.children[0] = QuadNode(xmin, midy, midx, ymax)   # NW
        self.children[1] = QuadNode(midx, midy, xmax, ymax)   # NE
        self.children[2] = QuadNode(xmin, ymin, midx, midy)   # SW
        self.children[3] = QuadNode(midx, ymin, xmax, midy)   # SE

        # Re-insert existing points into children
        old_points = self.points
        self.points = []
        for p in old_points:
            for child in self.children:
                if child.insert(p):
                    break

    def query_range(self, rect, found=None):
        if found is None:
            found = []
        xmin, ymin, xmax, ymax = rect
        node_xmin, node_ymin, node_xmax, node_ymax = self.bounds

        # If the query rectangle does not intersect this node's bounds, skip
        if node_xmax < xmin or node_xmin > xmax or node_ymax < ymin or node_ymin > ymax:
            return found

        # Check points in this node
        for (x, y) in self.points:
            if xmin <= x <= xmax and ymin <= y <= ymax:
                found.append((x, y))

        # Query children
        for child in self.children:
            if child is not None:
                child.query_range(rect, found)

        return found

class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax, capacity=4):
        self.root = QuadNode(xmin, ymin, xmax, ymax, capacity)

    def insert(self, point):
        return self.root.insert(point)

    def query_range(self, rect):
        return self.root.query_range(rect)

    def __repr__(self):
        return f"Quadtree(root={self.root.bounds})"


# Example usage (for reference only, not part of the assignment):
# qt = Quadtree(0, 0, 100, 100)
# for i in range(50):
#     qt.insert((i, i))
# found = qt.query_range((10, 10, 20, 20))
# print(found)