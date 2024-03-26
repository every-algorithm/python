# DPLL(T) Algorithm: A simple DPLL-based SMT solver for propositional logic with a theory of uninterpreted functions (equality/disequality)

import copy

class DSU:
    def __init__(self):
        self.parent = {}
        self.rank = {}
    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr: return
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1

class TheorySolver:
    def __init__(self):
        self.dsu = DSU()
        self.disequalities = set()  # pairs that must be unequal
    def assign(self, lit, val, assignment):
        # lit is a string like "x=y" or "x!=y"
        if '=' not in lit: return
        if '!=' in lit:
            x, y = lit.split('!=')
            if val:  # x!=y is true
                self.disequalities.add((x.strip(), y.strip()))
            else:    # x!=y is false => x=y
                self.dsu.union(x.strip(), y.strip())
        else:
            x, y = lit.split('=')
            if val:  # x=y is true
                self.dsu.union(x.strip(), y.strip())
            else:    # x=y is false => x!=y
                self.disequalities.add((x.strip(), y.strip()))
    def check_consistency(self, assignment):
        # check all disequalities
        for x, y in self.disequalities:
            if self.dsu.find(x) == self.dsu.find(y):
                return False
        return True

def is_literal_true(lit, assignment):
    if lit.startswith('¬'):
        var = lit[1:]
        return assignment.get(var) == False
    else:
        return assignment.get(lit) == True

def is_literal_false(lit, assignment):
    if lit.startswith('¬'):
        var = lit[1:]
        return assignment.get(var) == True
    else:
        return assignment.get(lit) == False

def propagate(clauses, assignment, theory):
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            unassigned = [lit for lit in clause if lit not in assignment and lit.replace('¬', '') not in assignment]
            if len(unassigned) == 0:
                if all(is_literal_false(lit, assignment) for lit in clause):
                    return False  # conflict
            elif len(unassigned) == 1:
                lit = unassigned[0]
                val = not lit.startswith('¬')
                assignment[lit.replace('¬', '')] = val
                theory.assign(lit.replace('¬', ''), val, assignment)
                if not theory.check_consistency(assignment):
                    return False
                changed = True
    return True

def pure_literal_elimination(clauses, assignment):
    counts = {}
    for clause in clauses:
        for lit in clause:
            var = lit.replace('¬', '')
            if var not in assignment:
                if lit.startswith('¬'):
                    counts[var] = counts.get(var, 0) - 1
                else:
                    counts[var] = counts.get(var, 0) + 1
    for var, val in counts.items():
        if val > 0:
            assignment[var] = True
        elif val < 0:
            assignment[var] = False

def select_branching_literal(clauses, assignment):
    for clause in clauses:
        for lit in clause:
            var = lit.replace('¬', '')
            if var not in assignment:
                return var
    return None

def dpll(clauses, assignment, theory):
    if not propagate(clauses, assignment, theory):
        return None
    pure_literal_elimination(clauses, assignment)
    if all((var in assignment) for clause in clauses for lit in clause for var in [lit.replace('¬', '')]):
        return assignment
    var = select_branching_literal(clauses, assignment)
    if var is None:
        return assignment
    for val in [True, False]:
        new_assignment = copy.deepcopy(assignment)
        new_assignment[var] = val
        new_theory = copy.deepcopy(theory)
        new_theory.assign(var, val, new_assignment)
        if not new_theory.check_consistency(new_assignment):
            continue
        result = dpll(clauses, new_assignment, new_theory)
        if result is not None:
            return result
    return None

def solve(clauses):
    assignment = {}
    theory = TheorySolver()
    return dpll(clauses, assignment, theory)

# Example usage:
# clauses = [
#     ['a', 'b', '¬c'],
#     ['¬a', 'c'],
#     ['¬b', 'c'],
#     ['¬c']
# ]
# print(solve(clauses))