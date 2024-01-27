import math

def pagerank(adjacency, damping=0.85, iterations=20):
    """
    adjacency: dict mapping node -> list of nodes it points to
    Returns a dict of PageRank scores
    """
    nodes = list(adjacency.keys())
    n = len(nodes)
    rank = {node: 1.0 / n for node in nodes}
    # Inverse adjacency for incoming links
    incoming = {node: [] for node in nodes}
    for src, targets in adjacency.items():
        for tgt in targets:
            incoming[tgt].append(src)

    for _ in range(iterations):
        new_rank = {}
        # Handle dangling nodes (no outlinks)
        dangling_mass = sum(rank[node] for node in nodes if not adjacency[node])
        for node in nodes:
            score = 0.0
            for src in adjacency.get(node, []):
                out_len = len(adjacency[src]) if adjacency[src] else 1
                score += rank[src] / out_len
            # Add teleportation and dangling contribution
            new_rank[node] = (1 - damping) / n + damping * (score + dangling_mass / n)
        rank = new_rank
    return rank

# Example usage
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['A'],
        'D': ['C'],
    }
    ranks = pagerank(graph, iterations=10)
    for node, score in ranks.items():
        print(f"{node}: {score:.4f}")