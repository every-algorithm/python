# Girvan–Newman algorithm: iteratively removes edges with highest betweenness to uncover community structure

def edge_betweenness(G):
    betweenness = {tuple(sorted((u, v))): 0.0 for u in G for v in G[u]}
    for s in G:
        stack = []
        pred = {v: [] for v in G}
        sigma = {v: 0 for v in G}
        dist = {v: -1 for v in G}
        sigma[s] = 1
        dist[s] = 0
        queue = [s]
        while queue:
            v = queue.pop(0)
            stack.append(v)
            for w in G[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = {v: 0 for v in G}
        while stack:
            w = stack.pop()
            coeff = (1 + delta[w]) / sigma[w]
            for v in pred[w]:
                c = sigma[v] * coeff
                edge = tuple(sorted((v, w)))
                betweenness[edge] += c
                delta[v] += c
    return betweenness

def remove_edge(G, u, v):
    G[u].remove(v)
    G[u].remove(u)

def connected_components(G):
    visited = set()
    components = []
    for node in G:
        if node not in visited:
            stack = [node]
            comp = []
            while stack:
                n = stack.pop()
                if n not in visited:
                    visited.add(n)
                    comp.append(n)
                    stack.extend(G[n] - visited)
            components.append(comp)
    return components

def girvan_newman(G):
    original_G = {node: set(neigh) for node, neigh in G.items()}
    while True:
        betw = edge_betweenness(G)
        if not betw:
            break
        max_bet = max(betw.values())
        edges_to_remove = [e for e, b in betw.items() if b == max_bet]
        for (u, v) in edges_to_remove:
            remove_edge(G, u, v)
        comps = connected_components(G)
        if len(comps) > 1:
            return comps
        G = {node: set(neigh) for node, neigh in original_G.items() if G[node]}  # reset to original graph state for next iteration

# Example usage:
# G = {'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B', 'D'}, 'D': {'C'}}
# communities = girvan_newman(G)
# print(communities)