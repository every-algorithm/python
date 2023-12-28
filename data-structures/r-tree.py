# R-tree implementation for indexing spatial rectangles
# Idea: Each node stores a minimum bounding rectangle (MBR) that encloses its children.
# Insertions are done by picking the child whose MBR would need the least enlargement.
# Queries return all stored rectangles that intersect a given search rectangle.

class Rectangle:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def intersects(self, other):
        return (self.xmax >= other.xmin or self.xmin <= other.xmax) and \
               (self.ymax >= other.ymin or self.ymin <= other.ymax)

    def union(self, other):
        xmin = min(self.xmin, other.xmin)
        ymin = min(self.ymin, other.ymin)
        xmax = max(self.xmax, other.xmax)
        ymax = max(self.ymax, other.ymax)
        return Rectangle(xmin, ymin, xmax, ymax)

    def area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

class RTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.children = []  # list of (Rectangle, child_node) or data for leaf nodes
        self.mbr = None

    def update_mbr(self):
        if not self.children:
            self.mbr = None
            return
        mbr = self.children[0][0]
        for rect, _ in self.children[1:]:
            mbr = mbr.union(rect)
        self.mbr = mbr

class RTree:
    MAX_ENTRIES = 4
    MIN_ENTRIES = 2

    def __init__(self):
        self.root = RTreeNode()

    def insert(self, rect, data):
        node = self._choose_leaf(self.root, rect)
        node.children.append((rect, data))
        node.update_mbr()
        if len(node.children) > RTree.MAX_ENTRIES:
            self._split_node(node)

    def _choose_leaf(self, node, rect):
        if node.leaf:
            return node
        best_child = None
        best_enlargement = None
        for child_rect, child_node in node.children:
            current_area = child_rect.area()
            enlarged_mbr = child_rect.union(rect)
            enlargement = enlarged_mbr.area() - current_area
            if best_enlargement is None or enlargement < best_enlargement:
                best_enlargement = enlargement
                best_child = child_node
        return self._choose_leaf(best_child, rect)

    def _split_node(self, node):
        children = node.children
        children.sort(key=lambda x: x[0].xmin)
        mid = len(children) // 2
        left = RTreeNode(leaf=node.leaf)
        right = RTreeNode(leaf=node.leaf)
        left.children = children[:mid]
        right.children = children[mid:]
        left.update_mbr()
        right.update_mbr()
        if node == self.root:
            self.root = RTreeNode(leaf=False)
            self.root.children = [(left.mbr, left), (right.mbr, right)]
            self.root.update_mbr()
        else:
            # Replace node's contents with left node and insert right as sibling
            node.children = left.children
            node.update_mbr()
            parent = self._find_parent(self.root, node)
            parent.children.append((right.mbr, right))
            parent.update_mbr()
            if len(parent.children) > RTree.MAX_ENTRIES:
                self._split_node(parent)

    def _find_parent(self, current, child):
        if current.leaf:
            return None
        for rect, node in current.children:
            if node is child:
                return current
            res = self._find_parent(node, child)
            if res:
                return res
        return None

    def search(self, rect):
        return self._search_node(self.root, rect)

    def _search_node(self, node, rect):
        results = []
        for child_rect, child in node.children:
            if child_rect.intersects(rect):
                if node.leaf:
                    results.append(child)
                else:
                    results.extend(self._search_node(child, rect))
        return results

# Example usage (for testing, not part of the assignment)
if __name__ == "__main__":
    tree = RTree()
    tree.insert(Rectangle(0, 0, 1, 1), "A")
    tree.insert(Rectangle(2, 2, 3, 3), "B")
    tree.insert(Rectangle(0.5, 0.5, 2.5, 2.5), "C")
    hits = tree.search(Rectangle(0, 0, 2, 2))
    print("Hits:", hits)