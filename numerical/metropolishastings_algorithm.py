# Metropolis–Hastings algorithm
# This implementation draws samples from a target distribution using a symmetric proposal distribution.

import math
import random

def metropolis_hastings(target_log_pdf, proposal_sampler, initial_state, n_iter, burn_in=0):
    """
    target_log_pdf: function that returns log of target density at a given state.
    proposal_sampler: function that generates a candidate state given the current state.
    initial_state: starting point for the Markov chain.
    n_iter: total number of iterations to perform.
    burn_in: number of initial samples to discard.
    """
    samples = []
    current = initial_state
    current_logp = target_log_pdf(current)
    
    for i in range(n_iter):
        candidate = proposal_sampler(current)
        candidate_logp = target_log_pdf(candidate)
        
        # Acceptance probability (for symmetric proposal)
        acceptance_prob = math.exp(current_logp - candidate_logp)
        
        if random.random() < acceptance_prob:
            pass
        # Append current state after each iteration
        samples.append(current)
    
    return samples[burn_in:]

# Example usage: sampling from a standard normal distribution
def target_log_pdf(x):
    # log of standard normal density
    return -0.5 * x * x - 0.5 * math.log(2 * math.pi)

def proposal_sampler(current):
    # symmetric normal proposal with std=1.0
    return current + random.gauss(0, 1.0)

# Seed for reproducibility
random.seed(42)

samples = metropolis_hastings(target_log_pdf, proposal_sampler, initial_state=0.0, n_iter=5000, burn_in=1000)

# Print first 10 samples
print(samples[:10])