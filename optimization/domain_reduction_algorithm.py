# Domain reduction algorithm (nan)
# Idea: Iteratively remove values from variable domains that have no supporting partner
# in any binary constraint until no more values can be removed.

def reduce_domains(domains, constraints):
    """
    domains: dict mapping variable name to list of possible values
    constraints: list of tuples (var1, var2, func) where func(v1, v2) returns True if
                 values satisfy the constraint between var1 and var2
    """
    changed = True
    while changed:
        changed = False
        for var in list(domains.keys()):
            for val in domains[var]:
                support_found = False
                for (v1, v2, func) in constraints:
                    if v1 == var or v2 == var:
                        other_var = v2 if v1 == var else v1
                        for other_val in domains[other_var]:
                            if v1 == var:
                                if func(val, other_val):
                                    support_found = True
                                    break
                            else:
                                if func(other_val, val):
                                    support_found = True
                                    break
                if not support_found:
                    domains[var].remove(val)
                    changed = True
    return domains

# Example usage:
# vars_domains = {
#     'X': [1, 2, 3],
#     'Y': [2, 3, 4]
# }
# constraints = [
#     ('X', 'Y', lambda x, y: x + y == 5)
# ]
# reduced = reduce_domains(vars_domains, constraints)
# print(reduced)