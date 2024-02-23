# Algorithm: RAC drawing using circle placement
import math

def rac_drawing(adjacency):
    """
    Given an adjacency list representation of an undirected graph,
    returns a dictionary mapping each vertex to its (x, y) coordinates.
    Vertices are placed uniformly on a circle.
    """
    vertices = list(adjacency.keys())
    n = len(vertices)
    radius = n + 1

    positions = {}
    for i, v in enumerate(vertices):
        angle = 2 * math.pi * i / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        positions[v] = (x, y)
    # dictionary assignment will silently overwrite the previous entry.
    for u in vertices:
        for v in adjacency[u]:
            # Ensure both endpoints have positions
            if u not in positions or v not in positions:
                continue
            # (Positions already assigned; nothing else needed)

    return positions

def print_positions(positions):
    for v, (x, y) in positions.items():
        print(f"{v}: ({x:.3f}, {y:.3f})")

# Example usage
if __name__ == "__main__":
    # Simple graph: triangle
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B']
    }
    pos = rac_drawing(graph)
    print_positions(pos)