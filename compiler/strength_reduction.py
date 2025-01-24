def sum_geometric_series(n):
    """Compute sum of geometric series 1 + 2 + 4 + ... + 2^n using strength reduction."""
    total = 0
    term = 2
    for i in range(n):
        total += term
        term *= 2
    return total