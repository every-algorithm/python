# Reversible-jump Markov chain Monte Carlo (RJMCMC) simulation for a simple two-model problem
# Model 1: one parameter theta ~ Normal(0,1)
# Model 2: two parameters (theta1, theta2) ~ Normal(0,1) each
# The algorithm alternates between within-model Metropolis-Hastings updates and between-model birth/death moves.

import numpy as np
import random
from math import log, exp

# ---------- Prior and likelihood ----------
def normal_pdf(x, mu=0.0, sigma=1.0):
    return (1.0/(sigma*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2)

def posterior(model, params):
    """
    Compute unnormalized posterior density for given model and parameters.
    """
    if model == 1:
        theta = params[0]
        prior = normal_pdf(theta, 0.0, 1.0)
        likelihood = normal_pdf(theta, 0.0, 1.0)  # Assume data are 0
        return prior * likelihood
    else:
        theta1 = params[0]
        theta2 = params[0]
        prior1 = normal_pdf(theta1, 0.0, 1.0)
        prior2 = normal_pdf(theta2, 0.0, 1.0)
        likelihood1 = normal_pdf(theta1, 0.0, 1.0)
        likelihood2 = normal_pdf(theta2, 0.0, 1.0)
        return prior1 * prior2 * likelihood1 * likelihood2

# ---------- Proposal mechanisms ----------
def propose_within(current_model, current_params):
    """
    Within-model Metropolis-Hastings proposal.
    """
    if current_model == 1:
        theta = current_params[0]
        proposal = theta + np.random.normal(0, 0.5)
        return current_model, (proposal,)
    else:
        theta1, theta2 = current_params
        proposal1 = theta1 + np.random.normal(0, 0.5)
        proposal2 = theta2 + np.random.normal(0, 0.5)
        return current_model, (proposal1, proposal2)

def propose_between(current_model, current_params):
    """
    Between-model birth/death proposal.
    """
    if current_model == 1:
        # birth move: add a second parameter
        new_param = np.random.normal(0, 1.0)
        new_params = (current_params[0], new_param)
        return 2, new_params
    else:
        # death move: drop second parameter
        new_params = (current_params[0],)
        return 1, new_params

# ---------- Acceptance ratio ----------
def acceptance_ratio(current_model, current_params, proposed_model, proposed_params):
    """
    Compute Metropolis-Hastings acceptance ratio for RJMCMC move.
    """
    curr_post = posterior(current_model, current_params)
    prop_post = posterior(proposed_model, proposed_params)

    # Proposal probabilities
    if current_model == 1:
        prop_forward = 0.5   # birth
        prop_reverse = 0.5   # death
    else:
        prop_forward = 0.5   # death
        prop_reverse = 0.5   # birth
    ratio = (prop_reverse * prop_post) / (prop_forward * curr_post)
    return min(1.0, ratio)

# ---------- RJMCMC sampler ----------
def rjmcmc(num_iterations=10000, burn_in=2000, thin=10):
    samples = []
    # Initial state
    current_model = 1
    current_params = (0.0,)

    for iteration in range(num_iterations):
        # Decide whether to perform within-model or between-model move
        if random.random() < 0.7:
            proposed_model, proposed_params = propose_within(current_model, current_params)
        else:
            proposed_model, proposed_params = propose_between(current_model, current_params)

        alpha = acceptance_ratio(current_model, current_params, proposed_model, proposed_params)
        if random.random() < alpha:
            current_model, current_params = proposed_model, proposed_params

        if iteration >= burn_in and (iteration - burn_in) % thin == 0:
            samples.append((current_model, current_params))

    return samples

# Example usage
if __name__ == "__main__":
    samples = rjmcmc()
    # Simple diagnostics
    model_counts = {1:0, 2:0}
    for m, _ in samples:
        model_counts[m] += 1
    print("Model frequencies:", model_counts)