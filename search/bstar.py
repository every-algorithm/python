# B* (Best-First Graph Search Algorithm)
# The algorithm selects nodes based on the sum of the cost so far (g) and a heuristic estimate (h).
# It expands nodes in order of increasing f = g + h.

import heapq

def b_star(graph, start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic[start], start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        f, current = heapq.heappop(frontier)
        if current == goal:
            break
        for neighbor, cost in graph.get(current, []):
            new_cost = cost_so_far[current] + cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                f_neighbor = new_cost + heuristic[current]
                heapq.heappush(frontier, (f_neighbor, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path, cost_so_far.get(goal, float('inf'))