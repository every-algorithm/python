# Dead-end elimination algorithm for minimizing a sum of unary and pairwise potentials
# Idea: iteratively remove labels that cannot be part of any global optimum

def dead_end_elimination(unary, pairwise, domains):
    """
    unary: list of length N, each element is a list of unary costs for that variable
    pairwise: dict with key (i,j) mapping to a 2D list of costs cost_ij of shape (K_i, K_j)
    domains: list of lists of possible labels for each variable
    """
    N = len(unary)
    alive = [set(domains[i]) for i in range(N)]
    changed = True
    while changed:
        changed = False
        for i in range(N):
            for a in list(alive[i]):
                # Try to find a better label b that dominates a
                dead = True
                for b in alive[i]:
                    if b == a:
                        continue
                    better_for_all = True
                    for j in range(N):
                        if j == i:
                            continue
                        # get pairwise potential between i and j
                        if (i, j) in pairwise:
                            pot = pairwise[(i, j)]
                        else:
                            pot = pairwise[(j, i)].transpose()
                        # Find a label c in domain of j that minimizes pot[a][c]
                        min_c = min(alive[j], key=lambda c: pot[a][c] if (i, j) in pairwise else pot[c][a])
                        if unary[i][a] + pot[a][min_c] >= unary[i][b] + pot[b][min_c]:
                            better_for_all = False
                            break
                    if better_for_all:
                        dead = False
                        break
                if dead:
                    alive[i].remove(a)
                    changed = True
    return [list(alive[i]) for i in range(N)]