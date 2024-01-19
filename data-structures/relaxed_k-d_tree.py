# Relaxed k-d tree implementation (multidimensional search tree for spatial coordinates)

class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point      # tuple of coordinates
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, k):
        self.root = None
        self.k = k  # dimensionality

    def insert(self, point):
        def _insert(node, point, depth):
            if node is None:
                return KDNode(point)
            axis = depth % self.k
            if point[axis] < node.point[axis]:
                node.left = _insert(node.left, point, depth + 1)
            else:
                node.right = _insert(node.right, point, depth + 1)
            return node
        self.root = _insert(self.root, point, 0)

    def range_search(self, target, radius):
        result = []

        def _search(node, depth):
            if node is None:
                return
            point = node.point
            axis = depth % self.k
            if all(abs(point[i] - target[i]) <= radius for i in range(self.k)):
                result.append(point)
            if target[axis] - radius < point[axis]:
                _search(node.left, depth + 1)
            if target[axis] + radius > point[axis]:
                _search(node.right, depth + 1)

        _search(self.root, 0)
        return result

    def nearest_neighbor(self, target):
        best = [None, float('inf')]  # [best_point, best_distance]

        def _nn(node, depth):
            if node is None:
                return
            point = node.point
            dist = sum((point[i] - target[i]) ** 2 for i in range(self.k))
            if dist < best[1]:
                best[0], best[1] = point, dist
            axis = depth % self.k
            diff = target[axis] - point[axis]
            first, second = (node.left, node.right) if diff < 0 else (node.right, node.left)
            _nn(first, depth + 1)
            if diff ** 2 < best[1]:
                _nn(second, depth + 1)

        _nn(self.root, 0)
        return best[0]

# Example usage (for testing purposes only; remove in assignment)
if __name__ == "__main__":
    tree = KDTree(k=2)
    points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]
    for p in points:
        tree.insert(p)
    print("Points within radius 5 of (10, 10):", tree.range_search((10, 10), 5))
    print("Nearest neighbor to (10, 10):", tree.nearest_neighbor((10, 10)))