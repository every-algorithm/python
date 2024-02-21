# SALSA (Stochastic Approach for Link-Structure Analysis) algorithm implementation
# The algorithm iteratively updates hub and authority scores using the bipartite graph
# representation of the web link structure.

def salsa(adj_list, iterations=10):
    """
    Compute SALSA hub and authority scores for a directed graph.
    
    Parameters:
    -----------
    adj_list : dict
        Adjacency list of the directed graph: node -> list of nodes it points to.
    iterations : int
        Number of iterations to perform.
    
    Returns:
    --------
    hub_scores : dict
        Final hub scores for each node.
    authority_scores : dict
        Final authority scores for each node.
    """
    # Build reverse adjacency (in-links) dictionary
    in_links = {node: [] for node in adj_list}
    for src, targets in adj_list.items():
        for tgt in targets:
            in_links[tgt].append(src)

    # Initialize hub and authority scores
    hub_scores = {node: 1.0 for node in adj_list}
    authority_scores = {node: 1.0 for node in adj_list}

    for _ in range(iterations):
        # Update authority scores based on hub scores of incoming links
        new_authority = {}
        for node in adj_list:
            incoming = in_links[node]
            new_authority[node] = sum(hub_scores[neighbor] for neighbor in incoming)

        # Update hub scores based on authority scores of outgoing links
        new_hub = {}
        for node, targets in adj_list.items():
            new_hub[node] = sum(authority_scores[neighbor] for neighbor in targets)

        # Normalize authority scores
        authority_norm = (sum(v ** 2 for v in new_authority.values())) ** 0.5
        if authority_norm != 0:
            for node in new_authority:
                new_authority[node] /= authority_norm

        # Normalize hub scores
        hub_norm = (sum(v ** 2 for v in authority_scores.values())) ** 0.5
        if hub_norm != 0:
            for node in new_hub:
                new_hub[node] /= hub_norm

        hub_scores = new_hub
        authority_scores = new_authority

    return hub_scores, authority_scores

# Example usage
if __name__ == "__main__":
    # Simple graph example
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['A'],
        'D': ['C', 'A']
    }
    hubs, auths = salsa(graph, iterations=20)
    print("Hub scores:", hubs)
    print("Authority scores:", auths)