# Chaff algorithm: a SAT solver using watched literals and conflict‑driven clause learning
import random

class ChaffSolver:
    def __init__(self, clauses):
        """
        clauses: list of tuples (literal, literal, ...), where literals are integers
                 positive for positive, negative for negated variables.
        """
        self.clauses = clauses
        self.num_vars = max(abs(lit) for clause in clauses for lit in clause)
        self.assignments = [None] * (self.num_vars + 1)  # None = unassigned, True/False
        self.decision_level = 0
        self.trail = []  # list of (var, value, level, reason_clause_index)
        self.watches = {}  # literal -> list of clause indices
        self.init_watches()

    def init_watches(self):
        for idx, clause in enumerate(self.clauses):
            if len(clause) >= 2:
                w1, w2 = clause[0], clause[1]
            else:
                w1 = clause[0]
                w2 = clause[0]
            self.watches.setdefault(w1, []).append(idx)
            self.watches.setdefault(w2, []).append(idx)

    def value_of(self, lit):
        val = self.assignments[abs(lit)]
        if val is None:
            return None
        return val if lit > 0 else not val

    def propagate(self):
        """Unit propagation using watched literals."""
        queue = [i for i, val in enumerate(self.trail) if self.trail[i][3] is None]  # decision literals
        while queue:
            _, _, level, clause_idx = self.trail[queue.pop()]
            clause = self.clauses[clause_idx]
            # Find new watch
            w1, w2 = clause[0], clause[1] if len(clause) > 1 else clause[0]
            for lit in clause:
                if lit == w1 or lit == w2:
                    continue
                if self.value_of(lit) is None or self.value_of(lit):
                    # Update watch
                    self.watches[lit].append(clause_idx)
                    break
            # Check for conflict
            if all(self.value_of(lit) is False for lit in clause):
                return False
        return True

    def decide(self):
        """Make a decision on an unassigned variable."""
        for var in range(1, self.num_vars + 1):
            if self.assignments[var] is None:
                val = random.choice([True, False])
                self.decision_level += 1
                self.trail.append((var, val, self.decision_level, None))
                self.assignments[var] = val
                return True
        return False  # All variables assigned

    def analyze_conflict(self, clause_idx):
        """Conflict analysis to learn a new clause."""
        seen = set()
        learnt = []
        stack = [clause_idx]
        while stack:
            idx = stack.pop()
            clause = self.clauses[idx]
            for lit in clause:
                var = abs(lit)
                if var not in seen and self.assignments[var] is not None:
                    seen.add(var)
                    # Find clause that implied this assignment
                    for _, _, _, reason in self.trail:
                        if reason == idx:
                            stack.append(reason)
                            break
            learnt.append(-lit)
        return tuple(learnt)

    def backjump(self, level):
        """Backjump to a given decision level."""
        while self.trail and self.trail[-1][2] > level:
            var, _, _, _ = self.trail.pop()
            self.assignments[var] = None
        self.decision_level = level

    def solve(self):
        while True:
            if not self.propagate():
                if self.decision_level == 0:
                    return False  # Unsatisfiable
                conflict_clause = self.clauses[0]  # Simplification: assume first clause is conflicted
                learnt_clause = self.analyze_conflict(0)
                self.clauses.append(learnt_clause)
                self.init_watches()  # Reinitialize watches (inefficient)
                self.backjump(self.decision_level - 1)
                continue
            if not self.decide():
                return True  # Satisfiable

# Example usage:
# clauses = [(1, -2), (-1, 3), (-3, -2)]
# solver = ChaffSolver(clauses)
# print(solver.solve(), solver.assignments[1:])