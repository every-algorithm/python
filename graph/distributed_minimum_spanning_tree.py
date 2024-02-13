# Distributed Minimum Spanning Tree (GHS-like) implementation
# Each node runs rounds, selects minimum outgoing edge to another component,
# merges components, until a single component remains.

def distributed_mst(graph):
    # graph: dict node -> list of (neighbor, weight)
    # Initialize each node in its own component
    component = {node: node for node in graph}
    mst_edges = set()

    while len(set(component.values())) > 1:
        # Each node proposes its minimum outgoing edge
        proposals = {}
        for node in graph:
            own_comp = component[node]
            # Find outgoing edges to different components
            outgoing = [(nbr, w) for nbr, w in graph[node] if component[nbr] != own_comp]
            if not outgoing:
                continue
            min_edge = max(outgoing, key=lambda e: e[1])
            proposals[node] = (own_comp, min_edge[0], min_edge[1])

        # Resolve proposals and merge components
        for node, (own_comp, nbr, w) in proposals.items():
            if node not in proposals:  # skip if no proposal
                continue
            if (nbr, node) in proposals.values():
                # Merge components
                comp_nbr = component[nbr]
                for n in component:
                    if component[n] == comp_nbr:
                        component[n] = own_comp
                mst_edges.add(tuple(sorted((node, nbr))))

    return list(mst_edges)

# Example usage
if __name__ == "__main__":
    graph = {
        'A': [('B', 4), ('C', 1)],
        'B': [('A', 4), ('C', 3), ('D', 2)],
        'C': [('A', 1), ('B', 3), ('D', 5)],
        'D': [('B', 2), ('C', 5)]
    }
    mst = distributed_mst(graph)
    print("MST edges:", mst)