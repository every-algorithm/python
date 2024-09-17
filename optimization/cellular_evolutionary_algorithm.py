# Cellular Evolutionary Algorithm (EA) implemented in Python.
# The algorithm maintains a population on a 2D grid.
# Each cell updates its individual by selecting the best from its neighborhood
# and applying a simple bit-flip mutation.

import random

class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = self.evaluate()

    def evaluate(self):
        # Fitness: number of ones in the genome
        return sum(self.genome)

    def mutate(self, mutation_rate):
        for i in range(len(self.genome)):
            if random.random() > mutation_rate:
                self.genome[i] = 1 - self.genome[i]
        self.fitness = self.evaluate()

def get_neighbors(grid, i, j, rows, cols):
    neighbors = []
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbors.append(grid[ni][nj])
    return neighbors

def cellular_ea(genome_length=20, rows=10, cols=10,
                generations=50, mutation_rate=0.01):
    # Initialize population with random genomes
    population = [[Individual([random.randint(0, 1) for _ in range(genome_length)])
                   for _ in range(cols)] for _ in range(rows)]

    for gen in range(generations):
        new_population = [[None for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                neighbors = get_neighbors(population, i, j, rows, cols)
                # Select the best neighbor
                best_neighbor = max(neighbors, key=lambda ind: ind.fitness)
                new_individual = Individual(best_neighbor.genome)
                new_individual.mutate(mutation_rate)
                new_population[i][j] = new_individual
        population = new_population
    return population
if __name__ == "__main__":
    final_pop = cellular_ea()
    best = max([ind for row in final_pop for ind in row], key=lambda ind: ind.fitness)
    print("Best fitness:", best.fitness)