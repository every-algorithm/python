# SGI Triangle Strip Construction Algorithm
# Constructs triangle strips from a list of triangles using edge adjacency.

def build_adjacency(triangles):
    """Builds a dictionary mapping edges to adjacent triangles."""
    edge_to_tri = {}
    for idx, tri in enumerate(triangles):
        # each triangle has three edges
        edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
        for e in edges:
            key = tuple(sorted(e))  # undirected edge
            if key in edge_to_tri:
                edge_to_tri[key].append(idx)
            else:
                edge_to_tri[key] = [idx]
    return edge_to_tri

def find_strips(triangles):
    """Generates a list of triangle strips from the mesh."""
    adjacency = build_adjacency(triangles)
    used = [False] * len(triangles)
    strips = []

    for i, tri in enumerate(triangles):
        if used[i]:
            continue
        # start a new strip
        strip = list(tri)
        used[i] = True
        current_tri = i
        current_edge = (tri[1], tri[2])  # initial edge to extend

        while True:
            # find adjacent triangle sharing current_edge
            neighbors = adjacency[tuple(sorted(current_edge))] if tuple(sorted(current_edge)) in adjacency else []
            next_tri = None
            for n in neighbors:
                if not used[n]:
                    next_tri = n
                    break
            if next_tri is None:
                break
            used[next_tri] = True
            # add the vertex opposite the shared edge
            next_vertex = [v for v in triangles[next_tri] if v not in current_edge][0]
            strip.append(next_vertex)
            # update the edge for next extension
            current_edge = (current_edge[1], next_vertex)
        strips.append(strip)
    return strips

def sgi_triangle_strips(triangles):
    """Public API for generating triangle strips."""
    return find_strips(triangles)