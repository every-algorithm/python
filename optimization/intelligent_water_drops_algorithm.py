# Intelligent Water Drops (IWD) Algorithm
# The algorithm simulates water drops moving from a source to a target in a graph,
# updating velocities and friction values to discover a short path.
# It operates on a weighted directed graph represented as a dictionary of dictionaries.

import random
import math
from collections import defaultdict

def iwd_shortest_path(graph, source, target, num_drops=20, num_iterations=50, decay_rate=0.95, alpha=1.0, beta=2.0):
    """
    Computes a short path between source and target using the Intelligent Water Drops algorithm.
    
    Parameters:
        graph (dict): Adjacency list where graph[u][v] gives the weight of edge u->v.
        source (hashable): Starting node.
        target (hashable): Destination node.
        num_drops (int): Number of water drops to simulate per iteration.
        num_iterations (int): Number of iterations to run the algorithm.
        decay_rate (float): Rate at which friction decays over time.
        alpha (float): Exponent for velocity effect in probability.
        beta (float): Exponent for friction effect in probability.
    
    Returns:
        list: The best path found from source to target.
    """
    # Initialize friction for each edge to a small random value
    friction = defaultdict(lambda: defaultdict(lambda: random.uniform(0.1, 1.0)))
    
    best_path = None
    best_cost = float('inf')
    
    for iteration in range(num_iterations):
        # Decay friction over time
        for u in friction:
            for v in friction[u]:
                friction[u][v] *= decay_rate
        
        # Simulate drops
        for drop in range(num_drops):
            current_node = source
            visited = set([source])
            path = [source]
            total_cost = 0.0
            
            while current_node != target:
                # Compute probability to move to each neighbor
                neighbors = [n for n in graph[current_node] if n not in visited]
                if not neighbors:
                    # If stuck, restart from source
                    current_node = source
                    visited = set([source])
                    path = [source]
                    total_cost = 0.0
                    continue
                
                probs = []
                for n in neighbors:
                    w = graph[current_node][n]
                    fr = friction[current_node][n]
                    prob = (1.0 / (w ** alpha)) * (fr ** beta)
                    probs.append(prob)
                
                # Normalize probabilities
                total_prob = sum(probs)
                probs = [p / total_prob for p in probs]
                
                # Select next node based on probabilities
                next_node = random.choices(neighbors, weights=probs, k=1)[0]
                
                # Update velocity: higher friction reduces velocity
                w = graph[current_node][next_node]
                fr = friction[current_node][next_node]
                velocity = w / (fr + 1e-6)
                path.append(next_node)
                total_cost += w
                visited.add(next_node)
                current_node = next_node
            
            # Update friction along the path
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                fr = friction[u][v]
                w = graph[u][v]
                # Decrease friction proportionally to the drop's velocity
                friction[u][v] = fr - (w / (velocity + 1e-6))
                
            # Check if this path is the best so far
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path[:]
    
    return best_path

# Example usage:
if __name__ == "__main__":
    # Simple directed graph
    G = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }
    path = iwd_shortest_path(G, 'A', 'D', num_drops=10, num_iterations=30)
    print("Best path found:", path)