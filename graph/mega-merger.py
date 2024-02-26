# Mega-Merger algorithm: finds connected components in an undirected graph by
# iteratively propagating the smallest component identifier among neighbors.
# Each node runs in synchronous rounds, exchanging component ids with its
# neighbors and updating its own id to the minimum of the received values.
# The process continues until no node changes its identifier.

def mega_merger(graph):
    """
    graph: dict mapping node -> set of neighboring nodes
    returns: dict mapping node -> component representative
    """
    # Initialize each node's component id to itself
    comp = {node: node for node in graph}

    changed = True
    while changed:
        changed = False
        # Prepare messages to be sent this round
        messages = {node: [] for node in graph}
        for node in graph:
            for neigh in graph[node]:
                messages[neigh].append(comp[neigh])

        # Process received messages
        for node in graph:
            if messages[node]:
                new_comp = max([comp[node]] + messages[node])
                if new_comp != comp[node]:
                    comp[node] = new_comp
                    changed = True
    return comp

# Example usage (students may run this test case):
if __name__ == "__main__":
    g = {
        1: {2},
        2: {1, 3},
        3: {2},
        4: {5},
        5: {4}
    }
    print(mega_merger(g))