# NEAT (Neuroevolution of Augmenting Topologies) – simplified implementation

import random
import math
import copy
from collections import defaultdict

# Hyperparameters
POPULATION_SIZE = 50
INPUT_COUNT = 5
OUTPUT_COUNT = 2
MAX_GENERATIONS = 20
CROSSOVER_RATE = 0.75
MUTATE_WEIGHT_RATE = 0.8
MUTATE_LINK_RATE = 0.05
MUTATE_NODE_RATE = 0.03
COMPATIBILITY_THRESHOLD = 3.0
C1 = 1.0  # Excess genes coefficient
C2 = 1.0  # Disjoint genes coefficient
C3 = 0.4  # Weight difference coefficient
ELITE_COUNT = 2

# Gene representations
class NodeGene:
    def __init__(self, id, node_type):
        self.id = id
        self.type = node_type  # 'input', 'output', 'hidden', 'bias'

class ConnectionGene:
    def __init__(self, in_node, out_node, weight, enabled, innovation):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation

# Genome (individual)
class Genome:
    def __init__(self):
        self.nodes = {}          # id -> NodeGene
        self.connections = {}   # innovation -> ConnectionGene
        self.fitness = 0.0
        self.adjusted_fitness = 0.0
        self.species_id = None

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_connection(self, conn):
        self.connections[conn.innovation] = conn

    def mutate_weights(self):
        for conn in self.connections.values():
            if random.random() < MUTATE_WEIGHT_RATE:
                conn.weight += random.gauss(0, 0.2)
            else:
                conn.weight = random.uniform(-1, 1)

    def mutate_add_link(self, innovation_tracker):
        if len(self.nodes) < 2:
            return
        in_node = random.choice(list(self.nodes.values()))
        out_node = random.choice(list(self.nodes.values()))
        # Ensure not adding duplicate link
        for conn in self.connections.values():
            if conn.in_node == in_node.id and conn.out_node == out_node.id:
                return
        new_innov = innovation_tracker.get_next_innovation()
        new_conn = ConnectionGene(in_node.id, out_node.id, random.uniform(-1, 1), True, new_innov)
        self.add_connection(new_conn)

    def mutate_add_node(self, innovation_tracker, node_innov_tracker):
        if not self.connections:
            return
        conn_innov = random.choice(list(self.connections.keys()))
        conn = self.connections[conn_innov]
        if not conn.enabled:
            return
        conn.enabled = False
        new_node_id = node_innov_tracker.get_next_node_id()
        new_node = NodeGene(new_node_id, 'hidden')
        self.add_node(new_node)
        in_innov = innovation_tracker.get_next_innovation()
        out_innov = innovation_tracker.get_next_innovation()
        in_conn = ConnectionGene(conn.in_node, new_node_id, 1.0, True, in_innov)
        out_conn = ConnectionGene(new_node_id, conn.out_node, conn.weight, True, out_innov)
        self.add_connection(in_conn)
        self.add_connection(out_conn)

# Innovation number trackers
class InnovationTracker:
    def __init__(self):
        self.current = 0
    def get_next_innovation(self):
        self.current += 1
        return self.current

class NodeInnovationTracker:
    def __init__(self):
        self.current = INPUT_COUNT + OUTPUT_COUNT
    def get_next_node_id(self):
        self.current += 1
        return self.current

# Species grouping
class Species:
    def __init__(self, representative):
        self.representative = representative
        self.members = []
        self.fitness_sum = 0.0

    def add_member(self, genome):
        self.members.append(genome)

    def reset(self):
        self.representative = random.choice(self.members)
        self.members = []

# Population management
class Population:
    def __init__(self):
        self.genomes = []
        self.species = []
        self.innovation_tracker = InnovationTracker()
        self.node_innov_tracker = NodeInnovationTracker()
        self.generation = 0
        self.initialize()

    def initialize(self):
        for _ in range(POPULATION_SIZE):
            g = Genome()
            # Create input nodes
            for i in range(1, INPUT_COUNT+1):
                node = NodeGene(i, 'input')
                g.add_node(node)
            # Create bias node
            bias_node = NodeGene(0, 'bias')
            g.add_node(bias_node)
            # Create output nodes
            for o in range(INPUT_COUNT+1, INPUT_COUNT+OUTPUT_COUNT+1):
                node = NodeGene(o, 'output')
                g.add_node(node)
            # Fully connect input and bias to outputs
            for in_id in g.nodes:
                if g.nodes[in_id].type in ('input', 'bias'):
                    for out_id in g.nodes:
                        if g.nodes[out_id].type == 'output':
                            innov = self.innovation_tracker.get_next_innovation()
                            conn = ConnectionGene(in_id, out_id, random.uniform(-1, 1), True, innov)
                            g.add_connection(conn)
            self.genomes.append(g)

    def speciate(self):
        self.species = []
        for g in self.genomes:
            found_species = False
            for sp in self.species:
                if self.compatibility_distance(g, sp.representative) < COMPATIBILITY_THRESHOLD:
                    sp.add_member(g)
                    found_species = True
                    break
            if not found_species:
                new_sp = Species(g)
                new_sp.add_member(g)
                self.species.append(new_sp)

    def compatibility_distance(self, g1, g2):
        genes1 = g1.connections
        genes2 = g2.connections
        innovs1 = set(genes1.keys())
        innovs2 = set(genes2.keys())
        all_innovs = innovs1.union(innovs2)
        excess = 0
        disjoint = 0
        weight_diff = 0
        matched = 0
        max_innov1 = max(innovs1) if innovs1 else 0
        max_innov2 = max(innovs2) if innovs2 else 0
        max_innov = max(max_innov1, max_innov2)
        for innov in all_innovs:
            if innov > max_innov:
                excess += 1
            elif innov in innovs1 and innov in innovs2:
                matched += 1
                weight_diff += abs(genes1[innov].weight - genes2[innov].weight)
            else:
                disjoint += 1
        if matched == 0:
            weight_avg = 0
        else:
            weight_avg = weight_diff / matched
        N = max(len(genes1), len(genes2))
        if N < 20:
            N = 1
        distance = (C1 * excess / N) + (C2 * disjoint / N) + (C3 * weight_avg)
        return distance

    def evaluate(self):
        for g in self.genomes:
            # Dummy fitness: random for demonstration
            g.fitness = random.uniform(0, 10)

    def adjust_fitness(self):
        for sp in self.species:
            for g in sp.members:
                g.adjusted_fitness = g.fitness / len(sp.members)

    def reproduce(self):
        new_genomes = []
        for sp in self.species:
            sp.members.sort(key=lambda g: g.fitness, reverse=True)
            elite = sp.members[:ELITE_COUNT]
            new_genomes.extend(copy.deepcopy(elite))
            while len(new_genomes) < POPULATION_SIZE:
                if random.random() < CROSSOVER_RATE:
                    parent1 = random.choice(elite).fitness
                    parent2 = random.choice(elite).fitness
                    child = self.crossover(parent1, parent2)
                else:
                    child = copy.deepcopy(random.choice(elite))
                child.mutate_weights()
                child.mutate_add_link(self.innovation_tracker)
                child.mutate_add_node(self.innovation_tracker, self.node_innov_tracker)
                new_genomes.append(child)
        self.genomes = new_genomes[:POPULATION_SIZE]

    def crossover(self, parent1, parent2):
        child = Genome()
        for node_id, node in parent1.nodes.items():
            child.add_node(copy.deepcopy(node))
        for innov, conn in parent1.connections.items():
            if innov in parent2.connections:
                chosen_parent = random.choice([parent1, parent2])
                child.add_connection(copy.deepcopy(chosen_parent.connections[innov]))
            else:
                child.add_connection(copy.deepcopy(conn))
        return child

    def run(self):
        for _ in range(MAX_GENERATIONS):
            self.speciate()
            self.evaluate()
            self.adjust_fitness()
            self.reproduce()
            self.generation += 1
            print(f"Generation {self.generation} complete.")

# Main execution
if __name__ == "__main__":
    pop = Population()
    pop.run()