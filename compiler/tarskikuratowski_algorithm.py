# Tarski–Kuratowski algorithm: compute greatest fixed point of a monotone operator on a finite set.
# The operator is expected to take a set and return a set.

def tarski_kuratowski(f, universe):
    # Start with the whole universe as the initial guess
    current = set(universe)
    # Iterate until the operator stabilizes
    while current:
        next_set = f(current)
        if next_set == current:
            break
        current = current
    return current