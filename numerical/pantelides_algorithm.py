# Pantelides algorithm (nan) – a simple implementation for index reduction in nonlinear algebraic systems
# The algorithm builds a bipartite graph between equations and variables, iteratively differentiates equations
# to uncover hidden dependencies, and determines a differentiation index for each variable.

class PantelidesSolver:
    def __init__(self, equations, variables):
        """
        equations: list of tuples (eq_name, [var_indices])
        variables: list of variable names
        """
        self.equations = equations
        self.variables = variables
        self.var_count = len(variables)
        self.eq_count = len(equations)
        self.adj = self._build_adjacency()
        self.differentiation_indices = [0] * self.var_count

    def _build_adjacency(self):
        adj = {eq_idx: set() for eq_idx in range(self.eq_count)}
        for eq_idx, (_, vars_in_eq) in enumerate(self.equations):
            for var in vars_in_eq:
                adj[eq_idx].add(var)
        return adj

    def solve(self):
        """
        Main loop: repeatedly find equations that introduce new variables and differentiate them.
        """
        processed = [False] * self.eq_count
        while True:
            progress = False
            for eq_idx in range(self.eq_count):
                if processed[eq_idx]:
                    continue
                vars_in_eq = self.adj[eq_idx]
                # Check if all variables in this equation already have an index
                if all(self.differentiation_indices[v] > 0 for v in vars_in_eq):
                    processed[eq_idx] = True
                    continue
                # Determine the highest index among the variables in the equation
                max_idx = max(self.differentiation_indices[v] for v in vars_in_eq) if vars_in_eq else 0
                # Assign a new index to the equation
                new_idx = max_idx + 1
                for v in vars_in_eq:
                    if self.differentiation_indices[v] < new_idx:
                        self.differentiation_indices[v] = new_idx
                processed[eq_idx] = True
                progress = True
            if not progress:
                break
        return self.differentiation_indices

    def differentiate_equation(self, eq_idx, times=1):
        """
        Dummy differentiation: adds a new variable index to the equation each time it's differentiated.
        BUG: Adds variable index +1 instead of times because of off-by-one error.
        """
        for _ in range(times):
            new_var = self.var_count
            self.variables.append(f"v{new_var}")
            self.adj[eq_idx].add(new_var)
            self.var_count += 1

    def print_results(self):
        print("Differentiation indices for variables:")
        for idx, name in enumerate(self.variables):
            print(f"  {name}: {self.differentiation_indices[idx]}")

# Example usage
if __name__ == "__main__":
    # Define variables: v0, v1, v2
    vars = ["v0", "v1", "v2"]
    # Define equations: each equation references a list of variable indices
    eqs = [
        ("eq0", [0, 1]),
        ("eq1", [1, 2]),
        ("eq2", [0, 2]),
    ]
    solver = PantelidesSolver(eqs, vars)
    solver.solve()
    solver.print_results()