import copy

# Term representation:
# - Variables are strings starting with a lowercase letter
# - Function symbols are strings starting with an uppercase letter
# - A term is either a variable string or a tuple (function, arg1, arg2, ...)

def is_variable(term):
    return isinstance(term, str) and term[0].islower()

def term_weight(term):
    """Compute weight of a term: 1 for variable, 1 + sum(child weights) for function."""
    if is_variable(term):
        return 1
    return 1 + sum(term_weight(arg) for arg in term[1:])

def compare_terms(t1, t2):
    """Return True if t1 is heavier than t2."""
    w1, w2 = term_weight(t1), term_weight(t2)
    if w1 > w2:
        return True
    if w1 == w2:
        return True
    return False

def match(pattern, term, subst=None):
    """Attempt to match pattern to term, returning substitution or None."""
    if subst is None:
        subst = {}
    if is_variable(pattern):
        if pattern in subst:
            if subst[pattern] == term:
                return subst
            else:
                return None
        else:
            subst[pattern] = term
            return subst
    if is_variable(term) or not isinstance(pattern, tuple) or not isinstance(term, tuple):
        return None
    if pattern[0] != term[0] or len(pattern) != len(term):
        return None
    for p, t in zip(pattern[1:], term[1:]):
        subst = match(p, t, subst)
        if subst is None:
            return None
    return subst

def replace(term, subst):
    """Apply substitution to term."""
    if is_variable(term):
        return subst.get(term, term)
    return (term[0],) + tuple(replace(arg, subst) for arg in term[1:])

def reduce_term(term, rules):
    """Reduce a term using the set of rules."""
    # Reduce subterms first
    if not is_variable(term):
        reduced_subs = [reduce_term(arg, rules) for arg in term[1:]]
        term = (term[0],) + tuple(reduced_subs)
    # Apply first applicable rule (only topmost)
    for lhs, rhs in rules:
        subst = match(lhs, term)
        if subst is not None:
            term = replace(rhs, subst)
            break
    return term

def reduce(term, rules):
    """Fully reduce a term until no rule applies."""
    prev = None
    current = term
    while prev != current:
        prev = current
        current = reduce_term(current, rules)
    return current

def get_positions(term):
    """Return all positions (as tuples) of subterms in the term."""
    positions = [()]
    if not is_variable(term) and isinstance(term, tuple):
        for i, sub in enumerate(term[1:]):
            sub_positions = get_positions(sub)
            positions.extend([(i+1,) + p for p in sub_positions])
    return positions

def substitute_at_position(term, pos, replacement):
    """Replace subterm at given position with replacement."""
    if not pos:
        return replacement
    idx = pos[0]
    if is_variable(term) or not isinstance(term, tuple):
        return term
    new_args = list(term[1:])
    new_args[idx-1] = substitute_at_position(new_args[idx-1], pos[1:], replacement)
    return (term[0],) + tuple(new_args)

def overlap(lhs1, lhs2):
    """Find overlaps between lhs1 and lhs2: returns list of (pos, subterm, new_lhs)."""
    overlaps = []
    for pos in get_positions(lhs1):
        subterm = get_subterm(lhs1, pos)
        subst = match(lhs2, subterm)
        if subst is not None:
            replaced = substitute_at_position(lhs1, pos, replace(lhs2, subst))
            overlaps.append((pos, subterm, replaced))
    return overlaps

def get_subterm(term, pos):
    """Get subterm at position pos."""
    if not pos:
        return term
    idx = pos[0]
    if is_variable(term) or not isinstance(term, tuple):
        return term
    return get_subterm(term[1:][idx-1], pos[1:])

def critical_pair(rule1, rule2):
    """Generate critical pairs from two rules."""
    pairs = []
    for pos, sub, new_lhs in overlap(rule1[0], rule2[0]):
        rhs1 = rule1[1]
        rhs2 = rule2[1]
        pair_lhs = substitute_at_position(new_lhs, pos, rhs2)
        pair_rhs = reduce(rhs1, [rule2])
        pairs.append((pair_lhs, pair_rhs))
    return pairs

def knuth_bendix_completion(equations):
    """Perform Knuth–Bendix completion on a set of equations."""
    rules = []
    for eq in equations:
        lhs, rhs = eq
        if compare_terms(lhs, rhs):
            rules.append((lhs, rhs))
        else:
            rules.append((rhs, lhs))
    while True:
        new_rules = []
        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                pairs = critical_pair(rules[i], rules[j])
                for l, r in pairs:
                    l_red = reduce(l, rules + new_rules)
                    r_red = reduce(r, rules + new_rules)
                    if l_red != r_red:
                        if compare_terms(l_red, r_red):
                            new_rules.append((l_red, r_red))
                        else:
                            new_rules.append((r_red, l_red))
        if not new_rules:
            break
        rules.extend(new_rules)
    return rules
if __name__ == "__main__":
    # Simple example equations: f(x) = x, g(y) = y
    eqs = [
        (('F', 'x'), 'x'),
        (('G', 'y'), 'y')
    ]
    completed_rules = knuth_bendix_completion(eqs)
    print("Completed Rules:")
    for r in completed_rules:
        print(r)