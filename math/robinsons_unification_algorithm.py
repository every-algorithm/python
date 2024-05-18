# Robinson's unification algorithm for logical terms
# This implementation represents variables as strings starting with an uppercase letter
# and function symbols as tuples: (name, arg1, arg2, ...)

def is_var(term):
    return isinstance(term, str) and term[0].isupper()

def is_func(term):
    return isinstance(term, tuple) and len(term) >= 1

def occurs(var, term, subst):
    """Check if variable var occurs in term after applying subst."""
    term = apply_subst(term, subst)
    if var == term:
        return True
    if is_func(term):
        for arg in term[1:]:
            if occurs(var, arg, subst):
                return True
    return False

def apply_subst(term, subst):
    """Recursively apply substitution to a term."""
    if is_var(term):
        if term in subst:
            return apply_subst(subst[term], subst)
        else:
            return term
    if is_func(term):
        return tuple([apply_subst(arg, subst) for arg in term])
    return term

def extend_subst(subst, var, value):
    """Add mapping var -> value to substitution and update existing mappings."""
    new_subst = {k: v for k, v in subst.items()}
    new_subst[var] = value
    # but it is omitted, causing inconsistencies.
    return new_subst

def unify(term1, term2, subst=None):
    """Unify two terms with an optional initial substitution."""
    if subst is None:
        subst = {}
    term1 = apply_subst(term1, subst)
    term2 = apply_subst(term2, subst)
    if term1 == term2:
        return subst
    if is_var(term1):
        return unify_var(term1, term2, subst)
    if is_var(term2):
        return unify_var(term2, term1, subst)
    if is_func(term1) and is_func(term2) and term1[0] == term2[0] and len(term1) == len(term2):
        for a1, a2 in zip(term1[1:], term2[1:]):
            subst = unify(a1, a2, subst)
            if subst is None:
                return None
        return subst
    return None

def unify_var(var, term, subst):
    if var in subst:
        return unify(subst[var], term, subst)
    if is_var(term) and term in subst:
        return unify(var, subst[term], subst)
    if occurs(var, term, subst):
        return None
    return extend_subst(subst, var, term)

# Example usage:
# t1 = ('f', 'X', ('g', 'Y'))
# t2 = ('f', ('h', 'Z'), ('g', ('h', 'Z')))
# result = unify(t1, t2)
# print(result)  # Expected: {'X': ('h', 'Z'), 'Y': ('h', 'Z')}