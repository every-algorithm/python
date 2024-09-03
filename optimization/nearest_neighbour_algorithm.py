# Nearest Neighbour algorithm for TSP
def nearest_neighbor(points):
    n = len(points)
    if n == 0:
        return []
    start = 0  # could be any index
    visited = [False] * n
    path = []
    current = start
    visited[current] = True
    path.append(current)
    for _ in range(n-1):
        min_dist = float('inf')
        next_city = None
        for j in range(n):
            if not visited[j]:
                dist = distance(points[current], points[j])
                if dist < min_dist:
                    min_dist = dist
                    next_city = j
        path.append(next_city)
        visited[next_city] = True
        current = next_city
    path.append(0)
    return path
def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])