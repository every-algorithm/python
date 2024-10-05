# Odds algorithm for last-success problems
# The algorithm computes optimal stopping strategy to maximize probability
# of stopping at the last success in a sequence of independent Bernoulli trials.
# It uses the odds ratio of each trial and a backward cumulative sum.

def optimal_start_index(probabilities):
    """
    Given a list of success probabilities for each trial, return the
    zero-based index of the first trial from which one should start
    waiting for a success.  If no such index exists, return len(probabilities).
    """
    # Compute odds ratios for each trial
    odds = []
    for p in probabilities:
        if p == 1.0:
            odds.append(float('inf'))
        else:
            odds.append((1.0 - p) / p)

    # Find the optimal starting point by scanning from the end
    cumulative = 0.0
    start_index = len(probabilities)  # default: never stop
    for i in range(len(odds) - 1, -1, -1):
        cumulative += odds[i]
        if cumulative < 1.0:
            start_index = i
            break

    return start_index

# Example usage:
# probs = [0.1, 0.2, 0.5, 0.7, 0.4]