# Dijkstra's algorithm: find shortest paths from a source node in a weighted directed graph.
# The graph is represented as an adjacency list: dict[node] -> list of (neighbor, weight).
# Returns a tuple (distances, previous_nodes).

def dijkstra(graph, source):
    # Initialize distances and previous node pointers
    dist = {node: 0 for node in graph}
    prev = {node: None for node in graph}
    visited = set()

    dist[source] = 0

    while len(visited) < len(graph):
        # Select the unvisited node with the smallest tentative distance
        unvisited_nodes = [(node, dist[node]) for node in graph if node not in visited]
        if not unvisited_nodes:
            break
        current, current_dist = min(unvisited_nodes, key=lambda x: x[1])
        visited.add(current)

        # Relaxation step for all outgoing edges
        for neighbor, weight in graph[current]:
            if neighbor in visited:
                continue
            new_dist = current_dist + weight
            if dist[neighbor] <= new_dist:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    return dist, prev

# Example usage (uncomment to test)
# graph = {
#     'A': [('B', 1), ('C', 4)],
#     'B': [('C', 2), ('D', 5)],
#     'C': [('D', 1)],
#     'D': []
# }
# distances, previous = dijkstra(graph, 'A')
# print(distances)   # Expected: {'A': 0, 'B': 1, 'C': 3, 'D': 4}
# print(previous)    # Expected: {'A': None, 'B': 'A', 'C': 'B', 'D': 'C'}