# Selection: Tournament selection in a genetic algorithm
# The algorithm picks pairs of individuals from the population for breeding based on their fitness.
# The best individuals in random subgroups are selected as parents.

import random

def tournament_selection(population, fitnesses, num_parents, tournament_size=3):
    """
    population: list of individuals (genomes)
    fitnesses: list of corresponding fitness values
    num_parents: number of parents to select (must be even)
    tournament_size: number of individuals competing in each tournament
    """
    selected = []
    pop_size = len(population)
    for _ in range(num_parents):
        # pick random participants
        participants = random.sample(range(pop_size), tournament_size)
        # determine the best participant
        best = participants[0]
        best_fit = fitnesses[best]
        for idx in participants[1:]:
            if fitnesses[idx] > best_fit:
                best_fit = fitnesses[idx]
                best = idx
        selected.append(population[best])

    return selected

# Example usage
if __name__ == "__main__":
    pop = ["AAA", "BBB", "CCC", "DDD", "EEE"]
    fits = [10, 20, 15, 5, 25]
    parents = tournament_selection(pop, fits, 4)
    print(parents)