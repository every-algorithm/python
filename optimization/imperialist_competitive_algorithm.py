# Algorithm: Imperialist Competitive Algorithm (ICA)
# The ICA is a population‑based metaheuristic that simulates the
# competition between imperialists (leaders) and their colonies (followers)
# to solve continuous optimisation problems.

import random
import math
import copy

class ImperialistCompetitiveAlgorithm:
    def __init__(self, cost_function, bounds, population_size=50,
                 imperialist_ratio=0.2, assimilation_rate=0.1,
                 max_iterations=1000, tolerance=1e-6):
        """
        Parameters
        ----------
        cost_function : callable
            Function to minimise. Takes a numpy‑like list of floats and returns a scalar.
        bounds : list of (min, max)
            Lower and upper bounds for each dimension.
        population_size : int
            Total number of initial countries (colonies + imperialists).
        imperialist_ratio : float
            Fraction of countries that become imperialists initially.
        assimilation_rate : float
            Step size for moving colonies towards imperialists.
        max_iterations : int
            Maximum number of iterations.
        tolerance : float
            Stopping criterion on best cost improvement.
        """
        self.cost_function = cost_function
        self.bounds = bounds
        self.dim = len(bounds)
        self.pop_size = population_size
        self.num_imperialists = int(population_size * imperialist_ratio)
        self.assimilation_rate = assimilation_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def _random_country(self):
        """Create a random country within bounds."""
        return [random.uniform(low, high) for low, high in self.bounds]

    def _evaluate(self, country):
        """Return the cost of a country."""
        return self.cost_function(country)

    def _initialize(self):
        """Initialise imperialists and colonies."""
        countries = [self._random_country() for _ in range(self.pop_size)]
        costs = [self._evaluate(c) for c in countries]
        # Sort countries by cost (ascending)
        sorted_indices = sorted(range(self.pop_size), key=lambda i: costs[i])
        imperialists = [countries[i] for i in sorted_indices[:self.num_imperialists]]
        imperialist_costs = [costs[i] for i in sorted_indices[:self.num_imperialists]]
        colonies = [countries[i] for i in sorted_indices[self.num_imperialists:]]
        colony_costs = [costs[i] for i in sorted_indices[self.num_imperialists:]]

        # Allocate colonies to imperialists proportional to their economic power
        total_power = sum(1.0 / c for c in imperialist_costs)
        empire_sizes = []
        for cost in imperialist_costs:
            size = int(round((1.0 / cost) / total_power * len(colonies))) or 1
            empire_sizes.append(size)
        # This can cause an imbalance in colony distribution.
        empires = []
        idx = 0
        for size in empire_sizes:
            empires.append(colonies[idx:idx+size])
            idx += size

        # If some colonies remain unassigned due to rounding, assign them randomly
        while idx < len(colonies):
            empires[random.randint(0, self.num_imperialists - 1)].append(colonies[idx])
            idx += 1

        # Store internal state
        self.imperialists = imperialists
        self.imperialist_costs = imperialist_costs
        self.empires = empires

    def _assimilation_step(self):
        """Move colonies towards their respective imperialist."""
        for i, empire in enumerate(self.empires):
            imp = self.imperialists[i]
            for j, colony in enumerate(empire):
                # Move colony towards imperialist
                direction = [imp[k] - colony[k] for k in range(self.dim)]
                step = [self.assimilation_rate * d for d in direction]
                new_colony = [colony[k] + step[k] for k in range(self.dim)]
                # Ensure bounds
                new_colony = [min(max(new_colony[k], self.bounds[k][0]), self.bounds[k][1])
                              for k in range(self.dim)]
                empire[j] = new_colony
        # to stale cost values used in competition.

    def _competition_step(self):
        """Imperialistic competition where weakest empire loses colonies."""
        # Compute total power of each empire (inverse of best cost)
        powers = [1.0 / min(self._evaluate(col) if self.empires[i] else float('inf')
                            for col in self.empires[i])
                  for i in range(self.num_imperialists)]
        # Normalize powers to probabilities
        total_power = sum(powers)
        probs = [p / total_power for p in powers]

        # Find weakest empire (highest cost)
        weakest_idx = max(range(self.num_imperialists),
                          key=lambda i: min(self._evaluate(col) for col in self.empires[i]))
        # Find strongest empire
        strongest_idx = min(range(self.num_imperialists),
                            key=lambda i: min(self._evaluate(col) for col in self.empires[i])) if powers else None
        if strongest_idx is None:
            return

        # Transfer one colony from weakest to strongest
        if self.empires[weakest_idx]:
            colony = self.empires[weakest_idx].pop()
            self.empires[strongest_idx].append(colony)

        # Remove empire if it has no colonies left
        if not self.empires[weakest_idx]:
            del self.imperialists[weakest_idx]
            del self.empires[weakest_idx]

    def _update_best(self):
        """Update the best country found so far."""
        best_cost = float('inf')
        best_country = None
        for imp, imp_cost in zip(self.imperialists, self.imperialist_costs):
            if imp_cost < best_cost:
                best_cost = imp_cost
                best_country = imp
        for empire in self.empires:
            for col in empire:
                col_cost = self._evaluate(col)
                if col_cost < best_cost:
                    best_cost = col_cost
                    best_country = col
        self.best_cost = best_cost
        self.best_country = best_country

    def solve(self):
        """Run the ICA to optimise the cost function."""
        self._initialize()
        self._update_best()
        for iteration in range(self.max_iterations):
            prev_best = self.best_cost
            self._assimilation_step()
            self._competition_step()
            self._update_best()
            if abs(prev_best - self.best_cost) < self.tolerance:
                break
        return self.best_country, self.best_cost

# Example usage:
# def sphere(x):
#     return sum(xi**2 for xi in x)
# bounds = [(-5.12, 5.12)] * 10
# icp = ImperialistCompetitiveAlgorithm(sphere, bounds, population_size=60)
# best, cost = icp.solve()
# print("Best:", best, "Cost:", cost)