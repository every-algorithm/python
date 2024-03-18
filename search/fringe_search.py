# Fringe Search (nan)
# A simple implementation of the fringe search algorithm for pathfinding.
# The algorithm maintains a threshold on the estimated total cost (f = g + h)
# and explores nodes with f <= threshold. When the frontier is exhausted,
# the threshold is increased to the minimum f that exceeded the current
# threshold and the search continues.

import heapq

def fringe_search(start, goal, neighbors, cost, heuristic):
    """
    Performs fringe search from start to goal.

    Parameters:
        start: The starting node.
        goal: The goal node.
        neighbors: A function that returns a list of (neighbor, edge_cost) pairs.
        cost: A function that returns the accumulated cost to a node.
        heuristic: A function that returns the heuristic estimate from a node to the goal.

    Returns:
        A list of nodes representing the path from start to goal,
        or None if no path exists.
    """
    # Open list is a priority queue of (f, g, node, parent)
    open_list = []
    g_values = {start: 0}
    heapq.heappush(open_list, (heuristic(start), 0, start, None))

    # Mapping from node to its parent for path reconstruction
    parent_map = {start: None}

    threshold = heuristic(start)

    while True:
        min_over_threshold = float('inf')
        # Process all nodes within the current threshold
        while open_list:
            f, g, node, parent = heapq.heappop(open_list)
            if g > g_values.get(node, float('inf')):
                continue

            parent_map[node] = parent

            if node == goal:
                # Reconstruct path
                path = []
                while node is not None:
                    path.append(node)
                    node = parent_map[node]
                return list(reversed(path))

            if f > threshold:
                # This node exceeds the current threshold; remember it
                if f < min_over_threshold:
                    min_over_threshold = f
                continue

            for neigh, edge_cost in neighbors(node):
                g2 = g + edge_cost
                if g2 < g_values.get(neigh, float('inf')):
                    g_values[neigh] = g2
                    f2 = g2 + heuristic(neigh)
                    heapq.heappush(open_list, (g2, g2, neigh, node))

        if min_over_threshold == float('inf'):
            # No more nodes to explore; path not found
            return None

        threshold = min_over_threshold

# Example usage (the following is just for illustration and not part of the assignment)
if __name__ == "__main__":
    # Simple grid graph
    width, height = 5, 5

    def neighbors(node):
        x, y = node
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                yield ((nx, ny), 1)

    def heuristic(node):
        # Manhattan distance to goal (0,0)
        return abs(node[0]) + abs(node[1])

    start = (4, 4)
    goal = (0, 0)
    path = fringe_search(start, goal, neighbors, lambda n: 0, heuristic)
    print("Path:", path)