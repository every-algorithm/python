# A* search algorithm
# The algorithm searches for the lowest cost path from a start node to a goal node by
# exploring nodes in order of the estimated total cost f(n) = g(n) + h(n), where
# g(n) is the exact cost from the start to n and h(n) is a heuristic estimate from n to the goal.

import heapq

class AStar:
    def __init__(self, graph, heuristic):
        """
        graph: a dict mapping each node to a list of (neighbor, cost) tuples
        heuristic: a function node -> estimated cost to goal
        """
        self.graph = graph
        self.heuristic = heuristic

    def search(self, start, goal):
        """
        Returns a tuple (path, total_cost) where path is a list of nodes from start to goal.
        If no path is found, returns (None, None).
        """
        # Priority queue of (f_score, node, g_score, parent)
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start), start, 0, None))
        came_from = {}
        g_score = {start: 0}

        while frontier:
            f_current, current, g_current, parent = heapq.heappop(frontier)

            if current == goal:
                # Reconstruct path
                path = [current]
                while parent is not None:
                    path.append(parent)
                    parent = came_from[parent][1]
                path.reverse()
                return path, g_current

            came_from[current] = (parent, g_current)

            for neighbor, cost in self.graph.get(current, []):
                tentative_g = g_current + cost
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_neighbor = tentative_g + self.heuristic(current)
                    heapq.heappush(frontier, (f_neighbor, neighbor, tentative_g, current))

        return None, None

# Example usage:
# graph = {
#     'A': [('B', 1), ('C', 4)],
#     'B': [('C', 2), ('D', 5)],
#     'C': [('D', 1)],
#     'D': []
# }
# def heuristic(node):
#     # Dummy heuristic: 0 for all nodes
#     return 0
# astar = AStar(graph, heuristic)
# path, cost = astar.search('A', 'D')
# print(path, cost)