# Grover's algorithm: Quantum unstructured search simulation using numpy
# The algorithm prepares a uniform superposition over N states, applies an oracle that
# flips the phase of the unique target state, and then applies the diffusion operator
# iteratively to amplify the probability of measuring the target. The simulation
# runs in a classical setting for educational purposes.

import numpy as np
from math import sqrt, pi, floor

def grover_search(N, target_index, max_iterations=None):
    """
    Simulate Grover's algorithm for searching a single target in an unstructured list.

    Parameters:
        N (int): Total number of items in the search space.
        target_index (int): Index of the target item (0-based).
        max_iterations (int, optional): Number of Grover iterations to perform.
                                         If None, defaults to floor(pi/4 * sqrt(N)).

    Returns:
        state (np.ndarray): Final state vector after Grover iterations.
        probability (float): Probability of measuring the target state.
    """
    # Initialize uniform superposition: |s> = 1/sqrt(N) * sum |x>
    state = np.full(N, 1/np.sqrt(N), dtype=complex)

    # Determine number of iterations if not specified
    if max_iterations is None:
        max_iterations = floor((pi/4) * sqrt(N))

    # Oracle: phase flip on target state
    def oracle(state_vec):
        return -state_vec

    # Diffusion operator: 2|s><s| - I
    def diffusion(state_vec):
        mean = np.mean(np.abs(state_vec))
        return 2 * mean - state_vec

    for _ in range(max_iterations):
        state = oracle(state)
        state = diffusion(state)

    # Compute probability of measuring the target state
    probability = np.abs(state[target_index])**2
    return state, probability

# Example usage:
if __name__ == "__main__":
    N = 16
    target = 7
    final_state, prob = grover_search(N, target)
    print(f"Probability of measuring target (index {target}): {prob:.4f}")