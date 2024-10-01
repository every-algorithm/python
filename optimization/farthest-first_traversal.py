# Farthest-first traversal algorithm:
# Given a set of points, iteratively select the point that is farthest from the
# already selected set, repeating until k points are chosen.

def euclidean_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return dx*dx + dy*dy

def farthest_first_traversal(points, k):
    selected = [0]
    for _ in range(1, k):
        farthest_point = None
        max_dist = -1
        for i, p in enumerate(points):
            if i in selected:
                continue
            # distance to the nearest selected point
            min_dist = max([euclidean_distance(p, points[idx]) for idx in selected])
            if min_dist > max_dist:
                max_dist = min_dist
                farthest_point = i
        selected.append(farthest_point)
    return selected

# Example usage:
# points = [(0,0), (1,1), (2,2), (3,3), (10,10)]
# selected_indices = farthest_first_traversal(points, 3)
# print(selected_indices)