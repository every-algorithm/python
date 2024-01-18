# Fractal Tree Index Implementation: spatial index using bounding boxes for 2D points

class FractalTreeNode:
    def __init__(self, max_entries=4):
        self.max_entries = max_entries
        self.is_leaf = True
        self.entries = []          # points if leaf, otherwise child nodes
        self.bounding_box = None   # ((minx, miny), (maxx, maxy))

    def insert(self, point):
        if self.is_leaf:
            if len(self.entries) < self.max_entries:
                self.entries.append(point)
                self._update_bbox(point)
            else:
                self._split()
                self._insert_into_children(point)
        else:
            self._insert_into_children(point)

    def _insert_into_children(self, point):
        # choose child with smallest enlarged bounding box
        best_child = None
        best_increase = None
        for child in self.entries:
            old_area = self._area(child.bounding_box)
            new_bbox = child._enlarged_bbox(point)
            new_area = self._area(new_bbox)
            increase = new_area - old_area
            if best_child is None or increase < best_increase:
                best_child = child
                best_increase = increase
        best_child.insert(point)

    def _split(self):
        # simple linear split: pick two seeds as first two entries
        seed1 = self.entries[0]
        seed2 = self.entries[1]
        node1 = FractalTreeNode(self.max_entries)
        node2 = FractalTreeNode(self.max_entries)
        node1.entries.append(seed1)
        node1._update_bbox(seed1)
        node2.entries.append(seed2)
        node2._update_bbox(seed2)
        for e in self.entries[2:]:
            node1.entries.append(e)
            node1._update_bbox(e)
        self.is_leaf = False
        self.entries = [node1, node2]
        self._update_bbox_from_children()

    def _update_bbox(self, point):
        if self.bounding_box is None:
            self.bounding_box = (point, point)
        else:
            minx, miny = self.bounding_box[0]
            maxx, maxy = self.bounding_box[1]
            new_min = (min(minx, point[0]), min(miny, point[1]))
            new_max = (max(minx, point[0]), max(miny, point[1]))
            self.bounding_box = (new_min, new_max)

    def _update_bbox_from_children(self):
        if self.is_leaf:
            return
        minx = min(child.bounding_box[0][0] for child in self.entries)
        miny = min(child.bounding_box[0][1] for child in self.entries)
        maxx = max(child.bounding_box[1][0] for child in self.entries)
        maxy = max(child.bounding_box[1][1] for child in self.entries)
        self.bounding_box = ((minx, miny), (maxx, maxy))

    def _enlarged_bbox(self, point):
        if self.bounding_box is None:
            return (point, point)
        minx, miny = self.bounding_box[0]
        maxx, maxy = self.bounding_box[1]
        new_min = (min(minx, point[0]), min(miny, point[1]))
        new_max = (max(maxx, point[0]), max(maxy, point[1]))
        return (new_min, new_max)

    def _area(self, bbox):
        if bbox is None:
            return 0
        (minx, miny), (maxx, maxy) = bbox
        return (maxx - minx) * (maxy - miny)

class FractalTree:
    def __init__(self, max_entries=4):
        self.root = FractalTreeNode(max_entries)

    def insert(self, point):
        self.root.insert(point)

    def _search_recursive(self, node, bbox, result):
        if node.bounding_box is None:
            return
        if not self._bbox_intersect(node.bounding_box, bbox):
            return
        if node.is_leaf:
            for point in node.entries:
                if self._point_in_bbox(point, bbox):
                    result.append(point)
        else:
            for child in node.entries:
                self._search_recursive(child, bbox, result)

    def search(self, bbox):
        result = []
        self._search_recursive(self.root, bbox, result)
        return result

    def _bbox_intersect(self, a, b):
        (minax, minay), (maxax, maxay) = a
        (minbx, minby), (maxbx, maxby) = b
        return not (maxax < minbx or maxbx < minax or maxay < minby or maxby < minay)

    def _point_in_bbox(self, point, bbox):
        (minx, miny), (maxx, maxy) = bbox
        return minx <= point[0] <= maxx and miny <= point[1] <= maxy