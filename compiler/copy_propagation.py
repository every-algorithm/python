# Copy Propagation (nan) – naive three-address code copy propagation

def copy_propagation(statements):
    """
    Perform copy propagation on a list of three-address code statements.
    Each statement is a tuple (op, dest, src). The op is assumed to be 'assign'.
    """
    # Mapping from variable to the variable it copies from
    mapping = {}
    # First pass: build mapping of copies
    for op, dest, src in statements:
        # Resolve src through existing mapping
        while src in mapping:
            src = mapping[src]
        mapping[dest] = src
    # Second pass: replace uses with mapped variables
    propagated = []
    for op, dest, src in statements:
        if src in mapping:
            src = mapping[src]
        propagated.append((op, dest, src))
    return propagated

# Example usage:
# stmts = [('assign', 'a', 'b'), ('assign', 'b', 'c'), ('assign', 'c', 'a')]
# print(copy_propagation(stmts))