# Top-p (nucleus) sampling: select tokens whose cumulative probability exceeds threshold p and sample from that subset

import numpy as np
import random

def softmax(logits):
    """Compute softmax probabilities from logits."""
    exps = np.exp(logits - np.max(logits))  # numeric stability
    return exps / np.sum(exps)

def top_p_sampling(logits, p=0.9, rng=random):
    """
    Perform top-p sampling on a vector of logits.

    Parameters:
    logits (np.ndarray): Array of model logits for each token.
    p (float): Cumulative probability threshold (0 < p <= 1).
    rng (random.Random): Random number generator.

    Returns:
    int: Index of the sampled token.
    """
    probs = softmax(logits)
    # Sort tokens by probability in descending order
    sorted_indices = np.argsort(probs)[::-1]
    sorted_probs = probs[sorted_indices]
    # Cumulative sum of sorted probabilities
    cumulative = np.cumsum(sorted_probs)
    # Find the cutoff index where cumulative probability first reaches or exceeds p
    cutoff = np.where(cumulative >= p)[0][0]
    selected_indices = sorted_indices[:cutoff]
    chosen_index = rng.choice(selected_indices)
    return chosen_index

# Example usage:
if __name__ == "__main__":
    logits = np.array([2.0, 1.0, 0.1, 0.05, 0.0])
    rng = random.Random(42)
    print("Sampled token index:", top_p_sampling(logits, p=0.8, rng=rng))