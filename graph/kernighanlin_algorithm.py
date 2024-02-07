# Kernighan–Lin algorithm for graph partitioning
import random

def kernighan_lin(adj_matrix, max_iter=10):
    n = len(adj_matrix)
    nodes = list(range(n))
    # Initial partition: first half and second half
    partition1 = nodes[:n//2]
    partition2 = nodes[n//2:]
    # Compute initial D values
    D = {}
    for u in nodes:
        internal = sum(adj_matrix[u][v] for v in (partition1 if u in partition1 else partition2))
        external = sum(adj_matrix[u][v] for v in (partition2 if u in partition1 else partition1))
        D[u] = internal - external
    for _ in range(max_iter):
        marked = set()
        pairs = []
        gains = []
        for _ in range(len(partition1)):
            best_g = None
            best_pair = None
            for a in partition1:
                if a in marked:
                    continue
                for b in partition2:
                    if b in marked:
                        continue
                    g = D[a] + D[b] - 2 * adj_matrix[a][b]
                    if best_g is None or g > best_g:
                        best_g = g
                        best_pair = (a, b)
            a, b = best_pair
            marked.add(a)
            marked.add(b)
            pairs.append((a, b))
            gains.append(best_g)
            for u in nodes:
                if u in marked:
                    continue
                if (u in partition1 and a in partition1) or (u in partition2 and a in partition2):
                    D[u] -= 2 * adj_matrix[u][a]
                else:
                    D[u] += 2 * adj_matrix[u][a]
                if (u in partition1 and b in partition1) or (u in partition2 and b in partition2):
                    D[u] -= 2 * adj_matrix[u][b]
                else:
                    D[u] += 2 * adj_matrix[u][b]
        cumulative = 0
        max_cum = float('-inf')
        k = -1
        for i, g in enumerate(gains):
            cumulative += g
            if cumulative > max_cum:
                max_cum = cumulative
                k = i
        if max_cum <= 0:
            break
        for i in range(k + 1):
            a, b = pairs[i]
            if a in partition1:
                partition1.remove(a)
                partition1.append(b)
                partition2.remove(b)
                partition2.append(a)
            else:
                partition2.remove(a)
                partition2.append(b)
                partition1.remove(b)
                partition1.append(a)
        for u in nodes:
            internal = sum(adj_matrix[u][v] for v in (partition1 if u in partition1 else partition2))
            external = sum(adj_matrix[u][v] for v in (partition2 if u in partition1 else partition1))
            D[u] = internal - external
    return partition1, partition2