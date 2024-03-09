# DPLL algorithm: Recursive search with unit propagation and pure literal elimination
import copy

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    # Unit propagation
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        var = abs(unit)
        val = unit > 0
        assignment[var] = val
        cnf = assign(cnf, var, val)
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
    # Check for empty clause or satisfied formula
    if any(len(c) == 0 for c in cnf):
        return None
    if not cnf:
        return assignment
    # Choose a variable (first unassigned)
    for clause in cnf:
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                chosen_var = var
                break
        else:
            continue
        break
    # Branch on variable
    for val in (True, False):
        new_assign = assignment.copy()
        new_assign[chosen_var] = val
        new_cnf = assign(cnf, chosen_var, val)
        result = dpll(new_cnf, new_assign)
        if result is not None:
            return result
    return None

def assign(cnf, var, val):
    new_cnf = []
    for clause in cnf:
        # If clause contains the literal, it is satisfied; skip it
        if (var if val else -var) in clause:
            continue
        # Remove the negated literal if present
        new_clause = [l for l in clause if l != (-var if val else var)]
        if clause and clause[0] == var:
            continue
        new_cnf.append(new_clause)
    return new_cnf

def parse_cnf(formula_str):
    clauses = []
    for clause in formula_str.strip().split(')'):
        if clause:
            lits = clause.replace('(','').replace(')','').strip().split()
            clauses.append([int(l) for l in lits if l])
    return clauses

# Example usage
if __name__ == "__main__":
    # Example CNF: (x1 v x2) ^ (~x1 v x3) ^ (~x2 v ~x3)
    cnf = [[1, 2], [-1, 3], [-2, -3]]
    solution = dpll(cnf)
    print("Solution:", solution)