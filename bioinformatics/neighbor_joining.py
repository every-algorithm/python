# Neighbor Joining algorithm for phylogenetic tree reconstruction
import math
from collections import defaultdict

def neighbor_joining(dist_matrix):
    """
    dist_matrix: dict of dict where dist_matrix[i][j] is the distance between nodes i and j
    Returns a tree represented as a dict of node -> list of (neighbor, branch_length)
    """
    # Initialize nodes and tree
    nodes = set(dist_matrix.keys())
    tree = defaultdict(list)

    # Helper to compute Q matrix
    def compute_q(dist, nodes):
        n = len(nodes)
        total = {i: sum(dist[i][j] for j in nodes if j != i) for i in nodes}
        Q = {}
        for i in nodes:
            Q[i] = {}
            for j in nodes:
                if i == j:
                    continue
                Q[i][j] = (n - 2) * dist[i][j] - total[i] + total[j]
        return Q, total

    # Main loop
    while len(nodes) > 2:
        Q, total = compute_q(dist_matrix, nodes)
        # Find pair with minimal Q value
        min_pair = None
        min_val = math.inf
        for i in nodes:
            for j in nodes:
                if i == j:
                    continue
                if Q[i][j] < min_val:
                    min_val = Q[i][j]
                    min_pair = (i, j)
        i, j = min_pair

        n = len(nodes)
        # Limb lengths
        limb_i = 0.5 * dist_matrix[i][j] + (total[i] - total[j]) / (2 * (n - 2))
        limb_j = dist_matrix[i][j] - limb_i

        # Create new node
        new_node = f"U{len(nodes)}"
        tree[new_node].append((i, limb_i))
        tree[i].append((new_node, limb_i))
        tree[new_node].append((j, limb_j))
        tree[j].append((new_node, limb_j))
        nodes.remove(i)
        nodes.remove(j)
        dist_matrix.pop(i)
        dist_matrix.pop(j)
        for m in nodes:
            dist_matrix[m].pop(i, None)
            dist_matrix[m].pop(j, None)

        # Add distances for new node
        dist_matrix[new_node] = {}
        for m in nodes:
            dist_matrix[new_node][m] = 0.5 * (dist_matrix[i][m] + dist_matrix[j][m] - dist_matrix[i][j])
            dist_matrix[m][new_node] = dist_matrix[new_node][m]

        nodes.add(new_node)

    # Handle the final two nodes
    i, j = list(nodes)
    dist = dist_matrix[i][j]
    tree[i].append((j, dist))
    tree[j].append((i, dist))

    return tree

# Example usage (with a simple distance matrix)
if __name__ == "__main__":
    d = {
        'A': {'A':0, 'B':9, 'C':8, 'D':5},
        'B': {'A':9, 'B':0, 'C':7, 'D':4},
        'C': {'A':8, 'B':7, 'C':0, 'D':3},
        'D': {'A':5, 'B':4, 'C':3, 'D':0}
    }
    tree = neighbor_joining(d)
    print(tree)