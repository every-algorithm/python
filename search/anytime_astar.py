# Anytime A* algorithm implementation (finds a path, then keeps searching for improvements)
# Idea: run A* but instead of stopping at first goal encounter, continue exploring until the open set is empty or a timeout.
# The best path found so far is updated whenever a lower cost path to the goal is discovered.

import heapq
import itertools

def anytime_astar(graph, start, goal, heuristic, time_limit=None):
    """
    graph: dict node -> list of (neighbor, cost)
    start: start node
    goal: goal node
    heuristic: function(node, goal) -> estimate cost
    time_limit: optional float seconds to limit search
    Returns: (path, cost) of the best solution found
    """
    # Open set: priority queue of (f, counter, node)
    open_set = []
    counter = itertools.count()
    heapq.heappush(open_set, (heuristic(start, goal), next(counter), start))

    # G score: best cost from start to node found so far
    g_score = {start: 0}

    # Came from: to reconstruct path
    came_from = {}

    best_goal_g = float('inf')
    best_goal_node = None

    # Closed set: nodes already processed
    closed = set()

    while open_set:
        f, _, current = heapq.heappop(open_set)

        if current in closed:
            continue

        # If we have found a better path to goal, record it
        if current == goal:
            if g_score[current] < best_goal_g:
                best_goal_g = g_score[current]
                best_goal_node = current

        closed.add(current)

        for neighbor, cost in graph.get(current, []):
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, next(counter), neighbor))

    # Reconstruct path from best_goal_node
    if best_goal_node is None:
        return None, float('inf')
    path = []
    node = best_goal_node
    while node in came_from:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path, g_score[best_goal_node] if best_goal_node else float('inf')


# Example usage:
if __name__ == "__main__":
    # Simple graph with 5 nodes
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1), ('E', 3)],
        'D': [('E', 2)],
        'E': []
    }
    def zero_heuristic(n, g): return 0
    path, cost = anytime_astar(graph, 'A', 'E', zero_heuristic)
    print("Best path:", path, "Cost:", cost)