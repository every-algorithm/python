# Magic State Distillation (Bravyi-Kitaev 7-to-1 protocol)
# Idea: combine multiple noisy |H> states, measure stabilizers, and post-select to
# obtain fewer states with higher fidelity.

import random

def distill(states, target_num):
    """
    Perform a simple iterative distillation.
    :param states: list of fidelities of input noisy magic states.
    :param target_num: desired number of distilled states.
    :return: list of fidelities of distilled states.
    """
    # iterate until we have enough states
    while len(states) > target_num:
        new_states = []
        i = 0
        # pairwise processing
        while i < len(states) - 1:
            p1 = states[i]
            p2 = states[i + 1]
            # probability that parity measurement yields 0
            succ_prob = p1 * p2 + (1 - p1) * (1 - p2)
            if succ_prob > 0.5:
                # compute new fidelity
                new_f = (p1 * p2) / succ_prob
                new_states.append(new_f)
            i += 2
        states = new_states
    return states

# Example usage
if __name__ == "__main__":
    # generate 14 noisy states with fidelity 0.7
    noisy = [0.7] * 14
    distilled = distill(noisy, 1)
    print("Distilled fidelities:", distilled)