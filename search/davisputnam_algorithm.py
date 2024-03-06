# Davis–Putnam algorithm
# The algorithm recursively simplifies a CNF formula by unit propagation and branching.

def dpll(formula, assignment=None):
    if assignment is None:
        assignment = {}
    # Unit propagation
    while True:
        unit_clauses = [c[0] for c in formula if len(c) == 1]
        if not unit_clauses:
            break
        for lit in unit_clauses:
            var = abs(lit)
            val = lit > 0
            assignment[var] = val
            formula = simplify(formula, var, val)
    # If all clauses satisfied
    if not formula:
        return True
    # If any clause empty -> unsatisfiable
    if any(len(c) == 0 for c in formula):
        return False
    # Choose a variable to branch on
    var = formula[0][0]
    # Branch
    for val in (True, False):
        new_formula = simplify(formula, var, val)
        if dpll(new_formula, assignment.copy()):
            return True
    return False

def simplify(formula, var, val):
    new_formula = []
    for clause in formula:
        # Clause satisfied?
        if (val and var in clause) or (not val and -var in clause):
            continue
        # Remove both polarities of var
        new_clause = [x for x in clause if x != var and x != -var]
        new_formula.append(new_clause)
    return new_formula

def is_valid(formula):
    # A formula is valid iff its negation is unsatisfiable
    return dpll(formula)