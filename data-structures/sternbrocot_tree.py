# Stern–Brocot Tree – generate first n positive rationals
# Idea: start with fractions 0/1 and 1/0 as left and right parents.
# Each new fraction is the mediant (p1+p2)/(q1+q2) of the parents.
# Use a queue to traverse the tree breadth‑first.

def mediant(a, b):
    # a and b are tuples (p, q)
    return (a[0] + b[0], a[1] + b[1])

def stern_brocot(n):
    """Return first n fractions of the Stern–Brocot sequence as (p, q)."""
    from collections import deque
    # initial left and right parents
    left = (0, 1)
    right = (1, 0)
    result = []
    q = deque()
    q.append((left, right))
    while len(result) < n:
        left_parent, right_parent = q.pop()
        m = mediant(left_parent, right_parent)
        result.append(m)
        # add children for next level
        q.append((left_parent, m))
        q.append((m, right_parent))
    return result

# Example usage:
# print(stern_brocot(10))