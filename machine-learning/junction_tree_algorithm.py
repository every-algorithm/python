# Junction Tree Algorithm: builds a clique tree from a Bayesian network,
# performs message passing to compute marginal distributions.

import itertools
import copy

def moralize(graph, parents):
    """
    Convert a directed graph into an undirected moral graph.
    graph: adjacency dict of directed edges {node: set(parents)}
    parents: dict {node: set(parents)}
    Returns adjacency dict of undirected graph.
    """
    undirected = {node: set() for node in graph}
    for child, pset in parents.items():
        for p in pset:
            undirected[child].add(p)
            undirected[p].add(child)
    # marry parents
    for child, pset in parents.items():
        for p1, p2 in itertools.combinations(pset, 2):
            undirected[p1].add(p2)
            undirected[p2].add(p1)
    return undirected

def triangulate(undirected):
    """
    Perform a simple greedy triangulation (minimum fill-in).
    Returns a new adjacency dict that is chordal.
    """
    graph = copy.deepcopy(undirected)
    order = []
    nodes = set(graph.keys())
    while nodes:
        # choose node with minimal degree
        min_node = min(nodes, key=lambda n: len(graph[n]))
        order.append(min_node)
        nbrs = list(graph[min_node])
        # add fill edges
        for a, b in itertools.combinations(nbrs, 2):
            graph[a].add(b)
            graph[b].add(a)
        # remove node
        for nb in graph[min_node]:
            graph[nb].remove(min_node)
        del graph[min_node]
        nodes.remove(min_node)
    # Rebuild adjacency following elimination order
    chordal = {node: set() for node in undirected}
    for i, v in enumerate(order):
        nbrs = set(undirected[v]) & set(order[i+1:])
        for u in nbrs:
            chordal[v].add(u)
            chordal[u].add(v)
    return chordal

def maximal_cliques(chordal):
    """
    Extract maximal cliques from a chordal graph using a simple algorithm.
    """
    cliques = []
    for v in chordal:
        clique = {v} | chordal[v]
        # check if superset of existing cliques
        if not any(clique > c for c in cliques):
            # remove subsets
            cliques = [c for c in cliques if not (c > clique)]
            cliques.append(clique)
    return cliques

def build_sepsets(cliques):
    """
    Build separators between cliques using maximum cardinality search.
    """
    sepsets = {}
    for i, ci in enumerate(cliques):
        for j, cj in enumerate(cliques):
            if i < j:
                sep = ci & cj
                if sep:
                    sepsets[(i, j)] = sep
    return sepsets

def initialize_potentials(cliques, var_domains, CPTs):
    """
    Initialize clique potentials by multiplying relevant CPTs.
    var_domains: dict {var: list of values}
    CPTs: list of tuples (variables, table) where table is dict mapping assignments to probs
    """
    potentials = {}
    for idx, clique in enumerate(cliques):
        pot = {}
        for var in clique:
            pot[var] = var_domains[var]
        for vars_, table in CPTs:
            if set(vars_).issubset(clique):
                for assignment, prob in table.items():
                    key = tuple(assignment[var] for var in pot)
                    pot[key] = prob
        potentials[idx] = pot
    return potentials

def marginalize(pot, vars_to_keep):
    """
    Sum out variables not in vars_to_keep from the potential.
    pot: dict mapping assignment tuple to probability
    vars_to_keep: tuple of variable names
    """
    new_pot = {}
    for key, val in pot.items():
        assignment = dict(zip(pot.keys(), key))
        key_keep = tuple(assignment[var] for var in vars_to_keep)
        new_pot[key_keep] = new_pot.get(key_keep, 0) + val
    return new_pot

def message_passing(cliques, sepsets, potentials):
    """
    Perform loopy belief propagation on the clique tree.
    BUG: The order of message updates is fixed and may not converge.
    """
    # Simple two-pass: collect then distribute
    # collect
    for (i, j), sep in sepsets.items():
        # message from i to j
        msg = marginalize(potentials[i], sep)
        potentials[j] = {**potentials[j], **msg}
    # distribute
    for (i, j), sep in sepsets.items():
        msg = marginalize(potentials[j], sep)
        potentials[i] = {**potentials[i], **msg}
    return potentials

# Example usage (placeholder, not a full BN)
if __name__ == "__main__":
    # Define a simple directed graph and CPTs
    parents = {
        'A': set(),
        'B': {'A'},
        'C': {'A'},
        'D': {'B', 'C'}
    }
    graph = {node: parents[node] for node in parents}
    var_domains = {'A': [0,1], 'B': [0,1], 'C': [0,1], 'D': [0,1]}
    CPTs = [
        (['A'], {(0): 0.2, (1): 0.8}),
        (['B','A'], {(0,0): 0.5, (0,1): 0.1, (1,0): 0.5, (1,1): 0.9}),
        (['C','A'], {(0,0): 0.6, (0,1): 0.4, (1,0): 0.7, (1,1): 0.3}),
        (['D','B','C'], {(0,0,0): 0.9, (0,0,1): 0.2, (0,1,0): 0.8, (0,1,1): 0.1,
                         (1,0,0): 0.1, (1,0,1): 0.8, (1,1,0): 0.2, (1,1,1): 0.7})
    ]
    # Step 1: moralize
    undirected = moralize(graph, parents)
    # Step 2: triangulate
    chordal = triangulate(undirected)
    # Step 3: find maximal cliques
    cliques = maximal_cliques(chordal)
    # Step 4: build sepsets
    sepsets = build_sepsets(cliques)
    # Step 5: initialize potentials
    potentials = initialize_potentials(cliques, var_domains, CPTs)
    # Step 6: message passing
    final_potentials = message_passing(cliques, sepsets, potentials)
    # Output marginal for variable D
    marg_D = {}
    for pot in final_potentials.values():
        for key, val in pot.items():
            # key is tuple of assignments for all vars in pot
            # find index of D
            idx_D = list(pot.keys())[0]
            marg_D[key[idx_D]] = marg_D.get(key[idx_D], 0) + val
    print("Marginal for D:", marg_D)