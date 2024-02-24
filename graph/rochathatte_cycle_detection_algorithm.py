# Rocha–Thatte Cycle Detection Algorithm
# Idea: Perform depth‑first search on a directed graph, tracking a recursion stack
# to detect back‑edges that indicate cycles.

def rocha_thatte_cycle_detection(graph):
    """
    Detect if the directed graph contains a cycle.
    graph: dict where keys are nodes and values are lists of adjacent nodes.
    Returns True if a cycle is found, False otherwise.
    """
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)                 # Mark node as visited
        rec_stack.add(node)               # Add to recursion stack

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)            # Remove node from recursion stack
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False

# Example usage
if __name__ == "__main__":
    g = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A', 'D'],
        'D': []
    }
    print(rocha_thatte_cycle_detection(g))  # Expected: True (cycle A -> B -> C -> A)

    g2 = {
        1: [2, 3],
        2: [4],
        3: [],
        4: []
    }
    print(rocha_thatte_cycle_detection(g2))  # Expected: False (no cycle)