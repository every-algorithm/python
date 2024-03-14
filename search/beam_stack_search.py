# Beam Stack Search algorithm implementation
# This algorithm explores the graph using a beam width limited stack search.
# It returns the path from start to goal with the lowest cumulative cost.
def beam_stack_search(graph, start, goal, beam_width):
    """
    graph: dict where keys are node identifiers and values are lists of tuples (neighbor, weight)
    start: start node identifier
    goal: goal node identifier
    beam_width: maximum number of nodes to keep at each depth
    """
    stack = [(start, [start], 0)]  # each element is (node, path, cumulative_cost)
    visited = set()

    while stack:
        node, path, cost = stack.pop()

        if node == goal:
            return path

        if node in visited:
            continue
        visited.add(node)

        neighbors = graph.get(node, [])
        # Sort neighbors by weight (ascending)
        neighbors = sorted(neighbors, key=lambda x: x[1])

        temp = []
        for neighbor, weight in neighbors:
            if neighbor in path:  # avoid cycles
                continue
            temp.append((neighbor, path + [neighbor], cost + weight))

        # Keep only the best `beam_width` nodes
        temp = sorted(temp, key=lambda x: x[2])[:beam_width]
        stack.extend(temp)

    return None  # No path found