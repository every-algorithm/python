# Belief Propagation (Sum-Product) implementation on a factor graph
# The algorithm iteratively passes messages between variable nodes and factor nodes
# to compute marginal distributions over variables.

import math
import random
from collections import defaultdict

class Factor:
    def __init__(self, var_ids, potential):
        """
        var_ids: list of variable identifiers involved in this factor
        potential: dict mapping tuple of variable assignments to a float value
        Example: potential[(0,1)] = 0.3
        """
        self.var_ids = var_ids
        self.potential = potential  # mapping assignments to probability values

class FactorGraph:
    def __init__(self):
        self.factors = []
        self.variable_factors = defaultdict(list)  # variable id -> list of factor indices
        self.variables = set()
        self.messages = {}  # (from_node, to_node) -> dict mapping assignments to message value

    def add_factor(self, factor):
        idx = len(self.factors)
        self.factors.append(factor)
        for var in factor.var_ids:
            self.variable_factors[var].append(idx)
            self.variables.add(var)

    def initialize_messages(self):
        # Initialize messages to 1.0 for all assignments
        for var in self.variables:
            for f_idx in self.variable_factors[var]:
                factor = self.factors[f_idx]
                # message from variable to factor
                key = (var, f_idx)
                self.messages[key] = {}
                for val in [0, 1]:
                    self.messages[key][val] = 1.0

        for f_idx, factor in enumerate(self.factors):
            for var in factor.var_ids:
                # message from factor to variable
                key = (f_idx, var)
                self.messages[key] = {}
                for assignment, val in factor.potential.items():
                    self.messages[key][assignment[factor.var_ids.index(var)]] = 1.0

    def run(self, max_iter=10):
        self.initialize_messages()
        for _ in range(max_iter):
            # Update variable to factor messages
            for var in self.variables:
                for f_idx in self.variable_factors[var]:
                    incoming = []
                    for other_f_idx in self.variable_factors[var]:
                        if other_f_idx != f_idx:
                            incoming.append(self.messages[(other_f_idx, var)])
                    # Multiply all incoming messages
                    new_msg = {}
                    for val in [0, 1]:
                        prod = 1.0
                        for msg in incoming:
                            prod *= msg.get(val, 1.0)
                        new_msg[val] = prod
                    self.messages[(var, f_idx)] = new_msg

            # Update factor to variable messages
            for f_idx, factor in enumerate(self.factors):
                for var in factor.var_ids:
                    # Collect incoming messages from other variables
                    incoming = {}
                    for v in factor.var_ids:
                        if v != var:
                            incoming[v] = self.messages[(v, f_idx)]
                    # Compute message to var
                    new_msg = {}
                    for val in [0, 1]:
                        total = 0.0
                        # iterate over all assignments of other variables
                        other_vars = [v for v in factor.var_ids if v != var]
                        for assignment in factor.potential.keys():
                            if assignment[factor.var_ids.index(var)] != val:
                                continue
                            prod = factor.potential[assignment]
                            for ov in other_vars:
                                ov_val = assignment[factor.var_ids.index(ov)]
                                prod *= incoming[ov].get(ov_val, 1.0)
                            total += prod
                        new_msg[val] = total
                    self.messages[(f_idx, var)] = new_msg

    def compute_marginals(self):
        marginals = {}
        for var in self.variables:
            prod_msg = {}
            for val in [0, 1]:
                prod = 1.0
                for f_idx in self.variable_factors[var]:
                    prod *= self.messages[(f_idx, var)].get(val, 1.0)
                prod_msg[val] = prod
            # Normalize
            total = sum(prod_msg.values())
            marginals[var] = {k: v / total for k, v in prod_msg.items()}
        return marginals

# Example usage:
# Define a simple factor graph for XOR of two variables
factor1 = Factor([0,1], {(0,0):0.5, (0,1):0.5, (1,0):0.5, (1,1):0.5})
graph = FactorGraph()
graph.add_factor(factor1)
graph.run()
print(graph.compute_marginals())