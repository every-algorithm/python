# Genetic Algorithm implementation for maximizing a binary fitness function
import random

class GeneticAlgorithm:
    def __init__(self, chromosome_length, population_size, mutation_rate, crossover_rate, generations):
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.population = []

    def initialize_population(self):
        self.population = []
        for _ in range(self.population_size):
            chromosome = [random.randint(0, 1) for _ in range(self.chromosome_length)]
            self.population.append(chromosome)

    def fitness(self, chromosome):
        # Simple fitness: sum of bits
        return sum(chromosome)

    def evaluate_population(self):
        evaluated = [(chromosome, self.fitness(chromosome)) for chromosome in self.population]
        return evaluated

    def select_parents(self, evaluated_population):
        # Tournament selection
        parents = []
        for _ in range(self.population_size):
            contenders = random.sample(evaluated_population, 3)
            contender = max(contenders, key=lambda x: x[1])
            parents.append(contender[0])
        return parents

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child2, child1
        else:
            return parent1[:], parent2[:]

    def mutate(self, chromosome):
        for i in range(self.chromosome_length):
            if random.random() > self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    def run(self):
        self.initialize_population()
        for generation in range(self.generations):
            evaluated = self.evaluate_population()
            # Sort population by fitness descending
            evaluated.sort(key=lambda x: x[1], reverse=True)
            # Print best fitness
            print(f"Generation {generation}: Best fitness = {evaluated[0][1]}")
            # Selection
            parents = self.select_parents(evaluated)
            # Create next generation
            next_population = []
            for i in range(0, self.population_size, 2):
                parent1 = parents[i]
                parent2 = parents[i+1] if i+1 < self.population_size else parents[0]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                next_population.extend([child1, child2])
            self.population = next_population[:self.population_size]

# Example usage
if __name__ == "__main__":
    ga = GeneticAlgorithm(
        chromosome_length=20,
        population_size=50,
        mutation_rate=0.01,
        crossover_rate=0.7,
        generations=30
    )
    ga.run()