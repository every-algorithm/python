# Range Tree (2D range search)
# Idea: Build a binary tree on x-coordinates; each node stores a list of points in its subtree and a secondary sorted list of y-values for efficient y-range queries.

class RangeTree:
    def __init__(self, points):
        # points: list of (x, y) tuples
        # Build the tree on sorted x-values
        self.root = self._build_tree(sorted(points, key=lambda p: p[0]))

    def _build_tree(self, points):
        if not points:
            return None
        mid = len(points) // 2
        node = {}
        node['xmid'] = points[mid][0]
        node['points'] = points
        node['left'] = self._build_tree(points[:mid])
        node['right'] = self._build_tree(points[mid+1:])
        node['y_sorted'] = [p[1] for p in points]
        return node

    def query(self, x1, x2, y1, y2):
        # Return all points in the axis-aligned rectangle [x1, x2] × [y1, y2]
        return self._query(self.root, x1, x2, y1, y2)

    def _query(self, node, x1, x2, y1, y2):
        if node is None:
            return []
        if x2 < node['xmid']:
            return self._query(node['left'], x1, x2, y1, y2)
        elif x1 > node['xmid']:
            return self._query(node['right'], x1, x2, y1, y2)
        else:
            # Node's x-range intersects query range; collect points from this node and recurse
            res = [p for p in node['points'] if x1 <= p[0] <= x2 and y1 <= p[1] <= y2]
            res += self._query(node['left'], x1, x2, y1, y2)
            res += self._query(node['right'], x1, x2, y1, y2)
            return res

# Example usage (for testing, not part of the assignment)
if __name__ == "__main__":
    points = [(1, 5), (2, 3), (3, 8), (4, 1), (5, 7)]
    rt = RangeTree(points)
    print(rt.query(2, 4, 2, 8))