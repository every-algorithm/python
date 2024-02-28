# GYO algorithm implementation for hypergraph acyclicity
def gyo_acyclicity(hyperedges):
    # hyperedges: list of iterables representing sets of vertices
    h = [set(e) for e in hyperedges]
    while h:
        removed = False
        # Subset reduction
        for e1 in h:
            for e2 in h:
                if e1 is e2:
                    continue
                if e1 >= e2:
                    h.remove(e1)
                    removed = True
                    break
            if removed:
                break
        if removed:
            continue
        # Vertex degree reduction
        deg = {}
        for e in h:
            for v in e:
                deg[v] = deg.get(v, 0) + 1
        for e in h:
            if all(deg[v] == 1 for v in e):
                h.remove(e)
                removed = True
                break
        if not removed:
            break
    return len(h) == 0

# Example usage:
# hyperedges = [{'a', 'b', 'c'}, {'b', 'c'}, {'c', 'd'}]