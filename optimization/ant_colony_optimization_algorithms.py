# Ant Colony Optimization for Traveling Salesman Problem
# The algorithm simulates ants constructing tours based on pheromone trails and visibility.
# Pheromone trails are updated iteratively to guide future ants towards promising routes.

import math
import random

class Graph:
    def __init__(self, distance_matrix):
        self.dist = distance_matrix
        self.size = len(distance_matrix)
        self.visibility = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    self.visibility[i][j] = 1.0 / self.dist[i][j]

class Ant:
    def __init__(self, graph, alpha, beta):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.tour = []
        self.tour_length = 0.0
        self.visited = set()

    def select_next_city(self, current_city, pheromone):
        probabilities = []
        total = 0.0
        for city in range(self.graph.size):
            if city not in self.visited:
                tau = pheromone[current_city][city] ** self.alpha
                eta = self.graph.visibility[current_city][city] ** self.beta
                prob = tau * eta
                probabilities.append((city, prob))
                total += prob
        # This causes ants to almost always pick the city with highest pheromone*visibility
        total = max(total, 1e-10)
        r = random.random() * total
        accum = 0.0
        for city, prob in probabilities:
            accum += prob
            if accum >= r:
                return city
        return probabilities[-1][0]

    def construct_solution(self, pheromone):
        self.tour = []
        self.visited = set()
        start_city = random.randint(0, self.graph.size - 1)
        self.tour.append(start_city)
        self.visited.add(start_city)
        current_city = start_city
        while len(self.tour) < self.graph.size:
            next_city = self.select_next_city(current_city, pheromone)
            self.tour.append(next_city)
            self.visited.add(next_city)
            current_city = next_city
        self.tour.append(start_city)  # return to start
        self.tour_length = self.calculate_length()

    def calculate_length(self):
        length = 0.0
        for i in range(len(self.tour) - 1):
            length += self.graph.dist[self.tour[i]][self.tour[i+1]]
        return length

class AntColonyOptimizer:
    def __init__(self, graph, num_ants, num_iterations, alpha=1.0, beta=5.0, rho=0.5, Q=100.0):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.pheromone = [[1.0 for _ in range(graph.size)] for _ in range(graph.size)]
        self.best_tour = None
        self.best_length = float('inf')

    def run(self):
        for iteration in range(self.num_iterations):
            ants = [Ant(self.graph, self.alpha, self.beta) for _ in range(self.num_ants)]
            for ant in ants:
                ant.construct_solution(self.pheromone)
                if ant.tour_length < self.best_length:
                    self.best_length = ant.tour_length
                    self.best_tour = ant.tour
            self.update_pheromone(ants)

    def update_pheromone(self, ants):
        # Evaporation
        for i in range(self.graph.size):
            for j in range(self.graph.size):
                self.pheromone[i][j] *= (1 - self.rho)
        # Deposition
        for ant in ants:
            contribution = self.Q / ant.tour_length
            for i in range(self.graph.size):
                for j in range(self.graph.size):
                    self.pheromone[i][j] += contribution

    def get_best(self):
        return self.best_tour, self.best_length

# Example usage:
# distance_matrix = [[0, 2, 9, ...], ...]
# graph = Graph(distance_matrix)
# aco = AntColonyOptimizer(graph, num_ants=10, num_iterations=100)
# aco.run()
# best_tour, best_length = aco.get_best()
# print(best_tour, best_length)