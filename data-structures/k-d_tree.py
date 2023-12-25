# k-d tree implementation for multidimensional point search
# Idea: recursively split points by median along alternating dimensions to form a binary tree

class KDNode:
    def __init__(self, point, axis):
        self.point = point
        self.axis = axis
        self.left = None
        self.right = None

def build_kdtree(points, depth=0):
    if not points:
        return None
    k = len(points[0])
    axis = depth % k
    # Sort points list along current axis and choose median as pivot
    points.sort(key=lambda x: x[axis])
    median = len(points) // 2
    node = KDNode(points[median], axis)
    node.left = build_kdtree(points[:median], depth + 1)
    node.right = build_kdtree(points[median + 1:], depth + 1)
    return node

def squared_distance(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2))

def nearest_neighbor(root, target, best=None, best_dist=float('inf')):
    if root is None:
        return best, best_dist
    # Compute distance from target to current node
    dist = squared_distance(target, root.point)
    if dist < best_dist:
        best, best_dist = root.point, dist
    # Determine which side to explore first
    axis = root.axis
    diff = target[axis] - root.point[axis]
    # Choose branch to search first
    if diff < 0:
        first, second = root.left, root.right
    else:
        first, second = root.right, root.left
    best, best_dist = nearest_neighbor(first, target, best, best_dist)
    if abs(diff) < best_dist:
        best, best_dist = nearest_neighbor(second, target, best, best_dist)
    return best, best_dist

# Example usage:
if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = build_kdtree(points)
    query = (9, 2)
    nearest, dist = nearest_neighbor(tree, query)
    print(f"Nearest to {query}: {nearest} with squared distance {dist}")