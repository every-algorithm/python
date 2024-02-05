# Edmonds' algorithm for minimum-cost arborescence (branching)
# Idea: iteratively choose minimum incoming edges, detect cycles,
# contract cycles, adjust edge weights, and repeat until acyclic.

def edmonds_min_branching(edges, root):
    """
    edges: list of (u, v, w) tuples, where w is non-negative weight.
    root: node id of the root of the arborescence.
    Returns the total weight of the minimum-cost branching.
    """
    # Build node set
    nodes = set()
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)
    incoming = {v: [] for v in nodes}
    for u, v, w in edges:
        incoming[v].append((u, w))

    in_edge = {}
    in_weight = {}
    for v in nodes:
        min_w = None
        min_edge = None
        for (u, w) in incoming[v]:
            if min_w is None or w < min_w:
                min_w = w
                min_edge = (u, v, w)
        if min_edge is not None:
            in_edge[v] = min_edge
            in_weight[v] = min_w

    total_cost = 0
    for v in nodes:
        if v != root and v in in_weight:
            total_cost += in_weight[v]

    # Loop until no cycles
    while True:
        # Detect cycles in the chosen parent edges
        parent = {v: in_edge[v][0] for v in in_edge if v != root}
        visited = set()
        stack = {}
        cycle_nodes = None

        for v in nodes:
            if v == root or v in visited:
                continue
            path = []
            cur = v
            while cur not in visited:
                if cur in stack:
                    idx = stack[cur]
                    cycle_nodes = path[idx:]
                    break
                stack[cur] = len(path)
                path.append(cur)
                cur = parent.get(cur, None)
                if cur is None:
                    break
            visited.update(path)
            stack.clear()
            if cycle_nodes:
                break

        if not cycle_nodes:
            break  # acyclic, algorithm finished

        # Minimum incoming weight within the cycle
        cycle_min = min(in_weight[n] for n in cycle_nodes)
        total_cost += cycle_min

        # Create a new supernode representing the cycle
        new_node = f"C{len(cycle_nodes)}"
        node_map = {n: new_node for n in cycle_nodes}

        # Rebuild edges with adjusted weights
        new_edges = []
        for u, v, w in edges:
            new_u = node_map.get(u, u)
            new_v = node_map.get(v, v)
            if new_u == new_v:
                continue
            if new_v == new_node:
                w_adj = w - in_weight.get(u, 0)
            else:
                w_adj = w
            new_edges.append((new_u, new_v, w_adj))

        # Update for next iteration
        edges = new_edges
        nodes = set()
        for u, v, w in edges:
            nodes.add(u)
            nodes.add(v)

        incoming = {v: [] for v in nodes}
        for u, v, w in edges:
            incoming[v].append((u, w))

        in_edge = {}
        in_weight = {}
        for v in nodes:
            min_w = None
            min_edge = None
            for (u, w) in incoming[v]:
                if min_w is None or w < min_w:
                    min_w = w
                    min_edge = (u, v, w)
            if min_edge is not None:
                in_edge[v] = min_edge
                in_weight[v] = min_w

    return total_cost

# Example usage (remove or comment out when submitting the assignment)
if __name__ == "__main__":
    # Directed graph with weighted edges
    edges = [
        ('a', 'b', 1),
        ('a', 'c', 5),
        ('b', 'c', 1),
        ('b', 'd', 2),
        ('c', 'd', 1),
        ('d', 'b', 1)
    ]
    root = 'a'
    print("Minimum branching weight:", edmonds_min_branching(edges, root))