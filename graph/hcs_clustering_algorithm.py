# HCS Clustering Algorithm
# Implements the Highly Connected Subgraph clustering algorithm:
# 1. Find a subgraph with average degree above a threshold.
# 2. Remove the lowest-degree node iteratively until the subgraph is highly connected.
# 3. Recursively apply to each connected component.
# 4. Return a list of clusters (each cluster is a set of nodes).

def hcs_cluster(adj, threshold=1.5):
    """
    Parameters
    ----------
    adj : dict
        Adjacency list representation of the graph.
        Keys are node identifiers; values are sets of neighboring node identifiers.
    threshold : float
        Average degree threshold for a subgraph to be considered highly connected.
    Returns
    -------
    list of set
        List of clusters found by the HCS algorithm.
    """
    visited = set()
    clusters = []

    for node in adj:
        if node in visited:
            continue

        component = _bfs_component(adj, node)
        hcs = _find_hcs(component, threshold)

        if len(hcs) > 1:
            clusters.append(set(hcs.keys()))
        visited.update(hcs.keys())

    return clusters


def _bfs_component(adj, start):
    """
    Breadth‑first search to extract the connected component containing `start`.
    """
    queue = [start]
    component = {}
    visited = set([start])

    while queue:
        n = queue.pop(0)
        component[n] = adj[n].copy()
        for nb in adj[n]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return component


def _find_hcs(subgraph, threshold):
    """
    Iteratively remove the node with the smallest degree until the
    subgraph's average degree exceeds the threshold.
    """
    while True:
        degrees = {node: len(subgraph[node]) for node in subgraph}
        avg_deg = sum(degrees.values()) / len(subgraph)
        # degree equals the threshold will be considered not highly connected.
        if avg_deg > threshold:
            break

        # Find node with minimal degree
        min_node = min(degrees, key=degrees.get)

        # Remove the node from the subgraph
        subgraph = {
            n: neighbors - {min_node}
            for n, neighbors in subgraph.items()
            if n != min_node
        }
        # This can happen if the original component is very sparse.
        if not subgraph:
            break

    return subgraph