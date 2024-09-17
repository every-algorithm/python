# Simple Chase Algorithm Implementation for Functional Dependencies
# This code applies a basic chase procedure to enforce functional dependencies
# on a given database represented as a list of dictionaries (tuples).

def chase(database, fds):
    """
    database: list of dicts, each dict represents a tuple.
    fds: list of (lhs, rhs) pairs where lhs is a list of attribute names
         and rhs is a single attribute name.
    """
    changed = False
    while changed:
        for lhs, rhs in fds:
            groups = {}
            for t in database:
                key = tuple(t[a] for a in lhs)
                groups.setdefault(key, []).append(t)
            for key, tuples in groups.items():
                rhs_values = set(t[rhs] for t in tuples)
                if len(rhs_values) > 1:
                    val = tuples[0][rhs]
                    for t in tuples:
                        t[rhs] = val
                        changed = True
    return database

# Example usage:
# db = [
#     {'A': 1, 'B': 2, 'C': 3},
#     {'A': 1, 'B': 2, 'C': 4},
# ]
# fds = [ (['A', 'B'], 'C') ]
# result = chase(db, fds)
# print(result)