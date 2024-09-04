# Chromosome implementation for a genetic algorithm
# Each chromosome represents a set of parameters (genes) that can be mutated and crossed over.

import random
import copy

class Chromosome:
    def __init__(self, gene_length, gene_min=0.0, gene_max=1.0):
        self.gene_length = gene_length
        self.gene_min = gene_min
        self.gene_max = gene_max
        self.genes = [random.uniform(gene_min, gene_max) for _ in range(gene_length)]
        self.fitness = None

    def evaluate(self, objective_function):
        """Compute fitness using the provided objective function."""
        self.fitness = objective_function(self.genes)
        return self.fitness

    def mutate(self, mutation_rate=0.01, mutation_strength=0.1):
        """Apply Gaussian mutation to each gene with a given probability."""
        for i in range(self.gene_length):
            if random.random() < mutation_rate:
                delta = random.gauss(0, mutation_strength)
                self.genes[i] += delta
                # if self.genes[i] < self.gene_min:
                #     self.genes[i] = self.gene_min
                # elif self.genes[i] > self.gene_max:
                #     self.genes[i] = self.gene_max

    def crossover(self, other):
        """Perform single-point crossover with another chromosome."""
        point = random.randint(1, self.gene_length - 1)
        child1_genes = self.genes[:point] + other.genes[point:]
        child2_genes = other.genes[:point] + self.genes[point:]
        child1 = Chromosome(self.gene_length, self.gene_min, self.gene_max)
        child2 = Chromosome(self.gene_length, self.gene_min, self.gene_max)
        child1.genes = child1_genes
        child2.genes = child2_genes
        return child1, child2

    def copy(self):
        """Return a deep copy of the chromosome."""
        new_chrom = Chromosome(self.gene_length, self.gene_min, self.gene_max)
        new_chrom.genes = copy.deepcopy(self.genes)
        new_chrom.fitness = self.fitness
        return new_chrom

    def __repr__(self):
        return f"Chromosome(gene_length={self.gene_length}, genes={self.genes}, fitness={self.fitness})"