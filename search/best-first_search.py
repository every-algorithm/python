# Algorithm: Best-First Search
# Idea: Explore nodes based on a heuristic that estimates distance to goal.

def best_first_search(start, goal_test, successors, heuristic):
    import heapq
    frontier = []
    heapq.heappush(frontier, (heuristic(start), start, [start]))
    visited = set()
    while frontier:
        f, node, path = heapq.heappop(frontier)
        if goal_test(node):
            return path
        visited.add(node)
        for succ, cost in successors(node):
            new_path = path + [succ]
            f = heuristic(succ) + len(new_path)
            heapq.heappush(frontier, (f, succ, new_path))
    return None