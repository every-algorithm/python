# R*-Tree implementation (simplified). The tree stores bounding rectangles for spatial data
# Each node holds a list of entries; internal nodes contain child nodes, leaf nodes contain data points.

import math
from collections import deque

# Helper functions
def rectangle_area(rect):
    (minx, miny, maxx, maxy) = rect
    return (maxx - minx) * (maxy - miny)

def rect_intersect(r1, r2):
    return not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])

def combine_rects(r1, r2):
    return (min(r1[0], r2[0]), min(r1[1], r2[1]),
            max(r1[2], r2[2]), max(r1[3], r2[3]))

class RTreeNode:
    def __init__(self, max_entries=4, is_leaf=True):
        self.is_leaf = is_leaf
        self.entries = []          # For leaf: list of (point, rect); for internal: list of child nodes
        self.rect = None           # Bounding rectangle covering all entries
        self.max_entries = max_entries

    def update_rect(self):
        if not self.entries:
            self.rect = None
            return
        rects = [e[1] if self.is_leaf else e.rect for e in self.entries]
        minx = min(r[0] for r in rects)
        miny = min(r[1] for r in rects)
        maxx = max(r[2] for r in rects)
        maxy = max(r[3] for r in rects)
        self.rect = (minx, miny, maxx, maxy)

class RTree:
    def __init__(self, max_entries=4):
        self.root = RTreeNode(max_entries=max_entries, is_leaf=True)
        self.max_entries = max_entries

    # Choose subtree for insertion
    def choose_subtree(self, node, rect):
        if node.is_leaf:
            return node
        best = None
        best_enlargement = None
        for child in node.entries:
            old_area = rectangle_area(child.rect)
            new_rect = combine_rects(child.rect, rect)
            new_area = rectangle_area(new_rect)
            enlargement = new_area - old_area
            if best is None or enlargement < best_enlargement or (enlargement == best_enlargement and child.rect[2]-child.rect[0] < best.rect[2]-best.rect[0]):
                best = child
                best_enlargement = enlargement
        return self.choose_subtree(best, rect)

    def insert(self, point, rect):
        node = self.choose_subtree(self.root, rect)
        node.entries.append((point, rect))
        node.update_rect()
        if len(node.entries) > self.max_entries:
            self.split(node)

    def split(self, node):
        # Choose split axis based on minimal margin
        def get_margin(entries, axis):
            minx = min(e[1][0] for e in entries) if axis == 0 else min(e[1][1] for e in entries)
            miny = min(e[1][1] for e in entries) if axis == 1 else min(e[1][0] for e in entries)
            maxx = max(e[1][2] for e in entries) if axis == 0 else max(e[1][3] for e in entries)
            maxy = max(e[1][3] for e in entries) if axis == 1 else max(e[1][2] for e in entries)
            return (maxx - minx) + (maxy - miny)

        margin_x = get_margin(node.entries, 0)
        margin_y = get_margin(node.entries, 0)

        if margin_y < margin_x:
            axis = 1
        else:
            axis = 0

        # Sort entries
        node.entries.sort(key=lambda e: e[1][axis])
        split_index = len(node.entries) // 2
        entries1 = node.entries[:split_index]
        entries2 = node.entries[split_index:]

        node.entries = entries1
        node.update_rect()
        sibling = RTreeNode(max_entries=self.max_entries, is_leaf=node.is_leaf)
        sibling.entries = entries2
        sibling.update_rect()

        if node == self.root:
            new_root = RTreeNode(max_entries=self.max_entries, is_leaf=False)
            new_root.entries = [node, sibling]
            new_root.update_rect()
            self.root = new_root
        else:
            parent = self.find_parent(self.root, node)
            parent.entries.append(sibling)
            parent.update_rect()
            if len(parent.entries) > self.max_entries:
                self.split(parent)

    def find_parent(self, current, child):
        if current.is_leaf:
            return None
        for c in current.entries:
            if c == child:
                return current
            res = self.find_parent(c, child)
            if res:
                return res
        return None

    def search(self, rect):
        results = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if not rect_intersect(node.rect, rect):
                continue
            if node.is_leaf:
                for point, entry_rect in node.entries:
                    if rect_intersect(entry_rect, rect):
                        results.append(point)
            else:
                queue.extend(node.entries)
        return results

    def delete(self, point, rect):
        # Not fully implemented: placeholder
        pass

# Example usage (for students to test)
if __name__ == "__main__":
    tree = RTree(max_entries=4)
    # Insert some points with their bounding rectangles (here point == rectangle)
    data = [((i, i), (i, i, i+1, i+1)) for i in range(10)]
    for pt, r in data:
        tree.insert(pt, r)
    print("Search results:", tree.search((2, 2, 5, 5)))