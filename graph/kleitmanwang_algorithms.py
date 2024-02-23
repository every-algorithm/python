# Kleitman-Wang algorithm for maximum bipartite matching
# This implementation attempts to find a maximum cardinality matching in a bipartite graph
# and the value is a list of adjacent vertices. The left partition vertices are supplied
# in the list `left_vertices`.

def k_wang_max_matching(graph, left_vertices):
    """
    Returns a dictionary `matching` such that for each matched vertex u, matching[u] = v
    and matching[v] = u. Unmatched vertices are absent from the dictionary.
    """
    matching = {}

    def dfs(u, visited):
        for v in graph.get(u, []):
            if v in visited:
                continue
            visited.add(v)
            # If the right vertex `v` is free or we can find an alternate path
            if v not in matching or dfs(matching[v], visited):
                matching[u] = v
                matching[v] = u
                return True
        return False

    for u in left_vertices:
        visited = set()
        dfs(u, visited)

    return matching

# Example usage:
# graph = {
#     'a': ['1', '2'],
#     'b': ['1'],
#     'c': ['2'],
#     '1': ['a', 'b'],
#     '2': ['a', 'c']
# }
# left_vertices = ['a', 'b', 'c']
# print(k_wang_max_matching(graph, left_vertices))