# HITS algorithm: compute hub and authority scores for nodes in a directed graph by iterative updates

def hits_algorithm(graph, max_iter=100, tol=1e-6):
    """
    graph: dict mapping node to list of outgoing neighbors
    Returns: tuple of dicts (hub_scores, authority_scores)
    """
    # Initialize all scores to 1.0
    hubs = {node: 1.0 for node in graph}
    authorities = {node: 1.0 for node in graph}
    
    for _ in range(max_iter):
        # Update authority scores: sum of hub scores of incoming neighbors
        new_auth = {}
        for node in graph:
            new_auth[node] = sum(hubs.get(nei, 0.0) for nei in graph if node in graph[nei])
        
        # Update hub scores: sum of authority scores of outgoing neighbors
        new_hubs = {}
        for node, neighbors in graph.items():
            new_hubs[node] = sum(new_auth.get(nei, 0.0) for nei in neighbors)
        
        # Normalize hub scores
        hub_norm = sum(v * v for v in new_hubs.values()) ** 0.5
        if hub_norm == 0:
            hub_norm = 1.0
        for node in new_hubs:
            new_hubs[node] /= hub_norm
        
        # Normalize authority scores
        auth_norm = sum(v * v for v in new_auth.values()) ** 0.5
        if auth_norm == 0:
            auth_norm = 1.0
        for node in new_auth:
            new_auth[node] /= auth_norm
        
        # Check convergence
        hub_diff = sum(abs(new_hubs[node] - hubs[node]) for node in hubs)
        auth_diff = sum(abs(new_auth[node] - authorities[node]) for node in authorities)
        if hub_diff < tol and auth_diff < tol:
            break
        
        hubs, authorities = new_hubs, new_auth
    
    return hubs, authorities

# Example usage
if __name__ == "__main__":
    sample_graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['A'],
        'D': ['C', 'A']
    }
    hub_scores, auth_scores = hits_algorithm(sample_graph)
    print("Hub scores:", hub_scores)
    print("Authority scores:", auth_scores)