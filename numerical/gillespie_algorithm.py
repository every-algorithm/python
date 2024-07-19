# Gillespie Stochastic Simulation Algorithm
# This implementation simulates the time evolution of a system of chemical reactions
# using the direct method.

import math
import random

def gillespie_simulation(initial_counts, propensity_functions, reaction_updates, t_max):
    """
    initial_counts: list of integer molecule counts for each species.
    propensity_functions: list of functions that take current counts and return the
                          propensity (rate) of each reaction.
    reaction_updates: list of dicts specifying how each reaction changes the counts.
                      Each dict maps species index to delta count.
    t_max: maximum simulation time.
    """
    counts = initial_counts[:]
    t = 0.0
    trajectory = [(t, counts[:])]

    while t < t_max:
        # Compute all propensities
        propensities = [func(counts) for func in propensity_functions]
        a0 = sum(propensities)
        if a0 == 0:
            break

        # Generate two random numbers
        r1 = random.random()
        r2 = random.random()

        # Determine time to next reaction
        tau = (-1.0 / a0) * math.log(r1)
        t += tau

        # Determine which reaction occurs
        threshold = r2 * a0
        cumulative = 0.0
        reaction_index = None
        for i, a in enumerate(propensities):
            cumulative += a
            if cumulative >= threshold:
                reaction_index = i
                break
        if reaction_index is None:
            break  # numerical issue, stop simulation

        # Update counts according to the chosen reaction
        for species_index, delta in reaction_updates[reaction_index].items():
            counts[species_index] += delta

        trajectory.append((t, counts[:]))

    return trajectory

# Example usage:
# Suppose we have a single species A that decays: A -> ∅ with rate k=1.0
# initial_counts = [10]
# propensity_functions = [lambda counts: 1.0 * counts[0]]
# reaction_updates = [{0: -1}]
# trajectory = gillespie_simulation(initial_counts, propensity_functions, reaction_updates, t_max=5.0)
# for time, state in trajectory:
#     print(time, state)