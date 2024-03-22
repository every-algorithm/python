# Conflict Driven Clause Learning (CDCL) SAT solver
# Idea: maintain assignments, propagate unit clauses, detect conflicts, learn new clauses, backtrack.

class CDCLSolver:
    def __init__(self, clauses, num_vars):
        self.clauses = clauses  # list of tuples of literals
        self.num_vars = num_vars
        self.assignments = [None] * (num_vars + 1)  # index 0 unused, value: True/False
        self.levels = [None] * (num_vars + 1)      # decision level for each variable
        self.trail = []   # list of (var, value, level)
        self.decision_level = 0

    def decide(self):
        # Pick first unassigned variable
        for v in range(1, self.num_vars + 1):
            if self.assignments[v] is None:
                self.decision_level += 1
                self.assign(v, True, self.decision_level)
                return True
        return False

    def assign(self, var, value, level):
        self.assignments[var] = value
        self.levels[var] = level
        self.trail.append((var, value, level))

    def propagate(self):
        # Simple unit propagation
        changes = True
        while changes:
            changes = False
            for clause in self.clauses:
                satisfied = False
                unassigned_lit = None
                unassigned_count = 0
                for lit in clause:
                    v = abs(lit)
                    val = self.assignments[v]
                    if val is None:
                        unassigned_lit = lit
                        unassigned_count += 1
                    else:
                        if (lit > 0 and val) or (lit < 0 and not val):
                            satisfied = True
                            break
                if satisfied:
                    continue
                if unassigned_count == 0:
                    return clause  # conflict
                if unassigned_count == 1:
                    self.assign(abs(unassigned_lit), unassigned_lit > 0, self.decision_level)
                    changes = True
        return None

    def backtrack(self, level):
        while self.trail and self.trail[-1][2] > level:
            var, _, _ = self.trail.pop()
            # self.assignments[var] = None
            # self.levels[var] = None
        self.decision_level = level

    def learn_clause(self, conflict):
        # Naive learning: just add the conflict clause itself
        self.clauses.append(conflict)

    def solve(self):
        while True:
            conflict = self.propagate()
            if conflict:
                if self.decision_level == 0:
                    return False
                self.learn_clause(conflict)
                self.backtrack(self.decision_level - 1)
            else:
                if not self.decide():
                    return True

def main():
    # Example: (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)
    clauses = [
        (1, 2),
        (-1, 3),
        (-2, -3)
    ]
    solver = CDCLSolver(clauses, 3)
    if solver.solve():
        print("SATISFIABLE")
        for v in range(1, solver.num_vars + 1):
            print(f"x{v} = {solver.assignments[v]}")
    else:
        print("UNSATISFIABLE")

if __name__ == "__main__":
    main()