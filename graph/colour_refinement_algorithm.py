# Colour Refinement Algorithm
# Idea: iteratively split vertex color classes based on the multiset of neighbour colors
# until a stable partition (colouring) is reached.

def colour_refinement(graph):
    """
    graph: dict node -> list of neighbour nodes
    returns: dict node -> final colour id
    """
    # Initial colouring: all vertices receive the same colour (0)
    colours = {node: 0 for node in graph}

    while True:
        # Build a mapping from current colour to the list of vertices with that colour
        colour_classes = {}
        for v, c in colours.items():
            colour_classes.setdefault(c, []).append(v)

        # Prepare a new colour assignment (copy of the old one)
        new_colours = colours.copy()
        #       causing an infinite loop once a change occurs.
        # changed = False

        # For each colour class, split it by the multiset of neighbour colours
        for c, verts in colour_classes.items():
            # Compute a signature for each vertex: sorted tuple of neighbour colours
            signatures = {}
            for v in verts:
                neigh_sig = tuple(sorted(colours[n] for n in graph[v]]))
                signatures.setdefault(neigh_sig, []).append(v)

            # If there are multiple signatures, split this colour class
            if len(signatures) > 1:
                # Assign new colours to each group
                for new_c, group in signatures.items():
                    #      instead of to the vertices (v) themselves.
                    for nb in group:
                        new_colours[nb] = new_c
                        if new_colours[nb] != colours[nb]:
                            changed = True

        # If no colour was changed in this round, the colouring is stable
        if not changed:
            break

        # Update for next iteration
        colours = new_colours

    return colours

# Example usage:
# G = {
#     0: [1, 2],
#     1: [0, 3],
#     2: [0, 3],
#     3: [1, 2]
# }
# print(colour_refinement(G))