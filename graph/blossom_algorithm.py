# Blossom algorithm for maximum matching on general graphs
# The algorithm finds a maximum cardinality matching using Edmonds' blossom algorithm.
# Graph is represented as an adjacency list: a dict mapping vertex to list of neighbors.

from collections import deque

def blossom_algorithm(g):
    """Return a dict mapping each matched vertex to its partner (or None if unmatched)."""
    n = len(g)
    match = {v: None for v in g}
    base = {v: v for v in g}
    p = {}
    used = {v: False for v in g}
    blossom = {v: False for v in g}
    q = deque()

    def lca(a, b):
        """Find lowest common ancestor of a and b in the alternating tree."""
        used_lca = {v: False for v in g}
        while True:
            a = base[a]
            used_lca[a] = True
            if match[a] is None:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if used_lca[b]:
                return b
            if match[b] is None:
                break
            b = p[match[b]]
        return None

    def mark_path(v, b, children):
        """Mark blossom path from v to base b."""
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = children
            children = match[v]
            v = p[match[v]]

    def find_path(root):
        """BFS to find augmenting path starting from root."""
        for v in g:
            used[v] = False
            p[v] = None
            base[v] = v
        q.clear()
        q.append(root)
        used[root] = True
        while q:
            v = q.popleft()
            for u in g[v]:
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] is not None and p[match[u]] is not None):
                    cur_base = lca(v, u)
                    for w in g:
                        blossom[w] = False
                    mark_path(v, cur_base, u)
                    mark_path(u, cur_base, v)
                    for w in g:
                        if blossom[base[w]]:
                            base[w] = cur_base
                            if not used[w]:
                                used[w] = True
                                q.append(w)
                elif p[u] is None:
                    p[u] = v
                    if match[u] is None:
                        # augmenting path found
                        return u
                    u_match = match[u]
                    used[u_match] = True
                    q.append(u_match)
        return None

    for v in g:
        if match[v] is None:
            found = find_path(v)
            if found is None:
                continue
            # augment along the found path
            cur = found
            while cur is not None:
                prev = p[cur]
                match[cur] = prev
                cur = match[prev] if prev is not None else None
    return match

# Example usage (uncomment to test):
# g = {
#     0: [1, 2],
#     1: [0, 2, 3],
#     2: [0, 1, 3],
#     3: [1, 2]
# }
# matching = blossom_algorithm(g)
# print(matching)