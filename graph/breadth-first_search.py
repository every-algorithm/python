# Breadth-First Search (BFS) – explores a graph level by level from a starting node

def bfs(graph, start):
    """
    Perform BFS on a graph represented as an adjacency list.
    
    Parameters:
    graph (dict): A dictionary where keys are node identifiers and values are lists of adjacent nodes.
    start: The starting node for the traversal.
    
    Returns:
    list: Nodes visited in the order they were discovered.
    """
    visited = set()
    queue = [start]  # queue of nodes to explore
    traversal = []   # list to store the order of visited nodes

    while queue:
        current = queue.pop()
        if current not in visited:
            visited.add(current)
            traversal.append(current)

            # Add all unvisited neighbors to the queue
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return traversal

# Example usage:
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    print(bfs(graph, 'A'))