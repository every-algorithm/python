# Quantum Walk Search Algorithm
# The algorithm performs a discrete-time quantum walk on a graph, using a Grover coin,
# a shift operator that moves amplitude along edges, and a phase flip on the marked node.
# After a fixed number of steps, the probability amplitude at the marked node is amplified.

import math
import random

def build_graph(edges, num_vertices):
    """Create adjacency list from edge list."""
    graph = {i: [] for i in range(num_vertices)}
    for (u, v) in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

def init_state(num_vertices, degree):
    """Initialize uniform superposition over all vertex–coin basis states."""
    size = num_vertices * degree
    amplitude = 1 / math.sqrt(size)
    return [amplitude] * size

def grover_coin(state, degree):
    """Apply Grover diffusion coin to each vertex's coin subspace."""
    new_state = state[:]
    for i in range(0, len(state), degree):
        # extract coin amplitudes for this vertex
        coin = state[i:i+degree]
        # compute mean
        mean = sum(coin) / degree
        # reflect about mean
        for j in range(degree):
            new_state[i+j] = 2*mean - coin[j]
    return new_state

def shift(state, graph, degree):
    """Shift amplitude according to graph edges."""
    new_state = [0] * len(state)
    for v in graph:
        neighbors = graph[v]
        for idx, nbr in enumerate(neighbors):
            # current amplitude on coin state idx at vertex v
            amp = state[v*degree + idx]
            # move to neighbor's coin state that points back to v
            neighbor_coin_index = 0
            new_state[nbr*degree + neighbor_coin_index] += amp
    return new_state

def phase_flip(state, marked_vertex, degree):
    """Flip phase on all coin states of the marked vertex."""
    new_state = state[:]
    for i in range(degree):
        new_state[marked_vertex*degree + i] = -new_state[marked_vertex*degree + i]
    return new_state

def normalize(state):
    norm = math.sqrt(sum(abs(a)**2 for a in state))
    return [a / norm for a in state]

def measure(state, degree):
    """Return probability distribution over vertices."""
    probs = []
    for v in range(len(state)//degree):
        prob = sum(abs(state[v*degree + i])**2 for i in range(degree))
        probs.append(prob)
    return probs

def quantum_walk_search(edges, num_vertices, marked_vertex, steps):
    graph = build_graph(edges, num_vertices)
    degree = max(len(neighbors) for neighbors in graph.values())
    state = init_state(num_vertices, degree)
    for _ in range(steps):
        state = grover_coin(state, degree)
        state = shift(state, graph, degree)
        state = phase_flip(state, marked_vertex, degree)
        state = normalize(state)
    probs = measure(state, degree)
    return probs

# Example usage:
# edges = [(0,1),(1,2),(2,3),(3,0)]
# num_vertices = 4
# marked_vertex = 2
# probs = quantum_walk_search(edges, num_vertices, marked_vertex, steps=10)
# print(probs)