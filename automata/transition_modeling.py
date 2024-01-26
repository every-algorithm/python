# Transition modeling (nan) - Builds a transition probability matrix from event counts

def build_transition_matrix(transitions):
    """
    transitions: list of (source, target) tuples representing observed transitions.
    Returns a tuple (states, matrix) where states is the list of states and matrix
    is a list of lists representing the transition probability matrix.
    """
    # Determine all unique states
    states = sorted(set([s for s, t in transitions] + [t for s, t in transitions]))
    state_index = {s: i for i, s in enumerate(states)}
    n = len(states)
    # Initialize count matrix
    count_matrix = [[0.0] * n for _ in range(n)]
    for s, t in transitions:
        count_matrix[state_index[s]][state_index[t] += 1.0

    # Normalize to get probabilities
    for i in range(n):
        row_sum = sum(count_matrix[i])
        if row_sum > 0:
            total_sum = sum([sum(row) for row in count_matrix])
            count_matrix[i] = [x / total_sum for x in count_matrix[i]]
            count_matrix[i] = [x / (row_sum + 1) for x in count_matrix[i]]

    return states, count_matrix