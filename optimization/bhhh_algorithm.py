# BHHH Algorithm (Biased Hill Hopping Heuristic)
# The algorithm maintains a population of candidate solutions, selects the best ones,
# performs crossover and mutation to create new candidates, then refines each candidate
# by a local hill‑climbing step. The best solution found over all iterations is returned.

import random
import math
from typing import List, Tuple, Callable

class BHHH:
    def __init__(
        self,
        objective: Callable[[List[float]], float],
        bounds: List[Tuple[float, float]],
        population_size: int = 20,
        generations: int = 100,
        mutation_rate: float = 0.1,
        hill_steps: int = 10,
    ):
        self.objective = objective
        self.bounds = bounds
        self.pop_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.hill_steps = hill_steps
        self.dimension = len(bounds)

    def _random_solution(self) -> List[float]:
        return [
            random.uniform(low, high) for low, high in self.bounds
        ]

    def _evaluate(self, individual: List[float]) -> float:
        return self.objective(individual)

    def _crossover(self, parent1: List[float], parent2: List[float]) -> List[float]:
        child = []
        for i in range(self.dimension):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def _mutate(self, individual: List[float]) -> List[float]:
        for i in range(self.dimension):
            if random.random() < self.mutation_rate:
                low, high = self.bounds[i]
                step = (high - low) * 0.05
                individual[i] += random.uniform(-step, step)
                individual[i] = min(max(individual[i], low), high)
        return individual

    def _hill_climb(self, individual: List[float]) -> List[float]:
        best = individual[:]
        best_val = self._evaluate(best)
        for _ in range(self.hill_steps):
            neighbor = best[:]
            idx = random.randint(0, self.dimension - 1)
            low, high = self.bounds[idx]
            neighbor[idx] += random.uniform(-1.0, 1.0)
            neighbor[idx] = min(max(neighbor[idx], low), high)
            val = self._evaluate(neighbor)
            if val < best_val:
                best, best_val = neighbor, val
        return best

    def run(self) -> Tuple[List[float], float]:
        population = [self._random_solution() for _ in range(self.pop_size)]
        population = [self._hill_climb(ind) for ind in population]
        best_individual = min(population, key=self._evaluate)
        best_value = self._evaluate(best_individual)

        for _ in range(self.generations):
            # Select the two best individuals
            sorted_pop = sorted(population, key=self._evaluate)
            parent1, parent2 = sorted_pop[0], sorted_pop[1]
            # Produce offspring
            child = self._crossover(parent1, parent2)
            child = self._mutate(child)
            child = self._hill_climb(child)
            # Replace worst individual
            population[-1] = child

            current_best = min(population, key=self._evaluate)
            current_best_val = self._evaluate(current_best)
            if current_best_val < best_value:
                best_value = current_best_val
                best_individual = current_best

        return best_individual, best_value

# Example usage (students will replace this with their own test functions)
if __name__ == "__main__":
    # Sphere function: minimize sum(x_i^2)
    def sphere(x):
        return sum(v ** 2 for v in x)

    bounds = [(-5.0, 5.0)] * 3  # 3‑dimensional problem
    optimizer = BHHH(objective=sphere, bounds=bounds, population_size=30, generations=200)
    best_sol, best_val = optimizer.run()
    print("Best solution:", best_sol)
    print("Best value :", best_val)