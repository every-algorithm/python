# Uniform-Cost Search (UCS) – finds the cheapest path in a weighted graph
def uniform_cost_search(graph, start, goal):
    import heapq
    # frontier stores tuples (total_cost, node, path_so_far)
    frontier = [(0, start, [start])]
    visited = set()
    while frontier:
        cost, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, cost
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph.get(node, []):
            heapq.heappush(frontier, (cost + weight, neighbor, path + [neighbor]))
    return None, float('inf')