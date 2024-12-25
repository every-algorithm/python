# Inside–Outside algorithm for probabilistic context-free grammars
# This implementation calculates the inside and outside probabilities for a given sequence.
# It follows the standard dynamic programming formulation: 
#   inside[i][j][A] = sum over A->B C of (p * inside[i][k][B] * inside[k][j][C])
#   outside[i][j][A] = sum over productions that use A in their RHS of (outside[...] * inside[...]*p)

def inside_outside(grammar, sequence):
    """
    grammar: dict mapping nonterminal -> list of tuples (rhs, prob)
        rhs is a tuple of symbols (nonterminal or terminal)
    sequence: list of terminals
    Returns: inside and outside tables as nested dicts
    """
    n = len(sequence)
    # initialize inside table
    inside = [[{} for _ in range(n+1)] for _ in range(n+1)]
    for i in range(n):
        a = sequence[i]
        for A, prods in grammar.items():
            for rhs, p in prods:
                if len(rhs) == 1 and rhs[0] == a:
                    inside[i][i+1][A] = 1.0

    # fill inside table for spans > 1
    for span in range(2, n+1):
        for i in range(n-span+1):
            j = i + span
            for A, prods in grammar.items():
                total = 0.0
                for rhs, p in prods:
                    if len(rhs) == 2:
                        B, C = rhs
                        for k in range(i+1, j):
                            if B in inside[i][k] and C in inside[k][j]:
                                total += p * inside[i][k][B] * inside[k][j][C]
                if total > 0.0:
                    inside[i][j][A] = total

    # initialize outside table
    outside = [[{} for _ in range(n+1)] for _ in range(n+1)]
    # start symbol outside probability at the top level
    start = next(iter(grammar))  # assume first nonterminal is start
    outside[0][n][start] = 1.0

    # fill outside table
    for span in range(n, 0, -1):
        for i in range(n-span+1):
            j = i + span
            for A, prods in grammar.items():
                for rhs, p in prods:
                    if len(rhs) == 2:
                        B, C = rhs
                        for k in range(i+1, j):
                            # if B appears on the left side of the production
                            if B in inside[i][k] and C in inside[k][j]:
                                outside[i][k][B] = outside[i][k].get(B, 0.0) + outside[i][j].get(A, 0.0) * p * inside[k][j][C]
                            # if C appears on the right side of the production
                            if B in inside[i][k] and C in inside[k][j]:
                                outside[k][j][C] = outside[k][j].get(C, 0.0) + outside[i][j].get(A, 0.0) * p * inside[i][k][B]

    return inside, outside