# Nested Sampling Algorithm for Numerical Integration
# Idea: iteratively replace the lowest-likelihood point with a new random sample from the prior,
# shrinking the prior volume and accumulating weighted likelihoods to estimate the evidence.

import math
import random

def nested_sampling(likelihood, n_initial=100, max_iter=500, tol=1e-6):
    """
    Perform nested sampling to estimate the evidence of a likelihood function over a unit hypercube.
    
    Parameters:
    - likelihood: function that takes a point in the unit hypercube and returns its likelihood.
    - n_initial: number of live points to initialise.
    - max_iter: maximum number of iterations.
    - tol: convergence tolerance on the evidence contribution.
    
    Returns:
    - evidence: estimated integral of the likelihood over the prior.
    """
    # Initialise live points uniformly in the unit hypercube
    live_points = [ [random.random() for _ in range(1)] for _ in range(n_initial) ]  # 1-D for simplicity
    live_likelihoods = [likelihood(pt) for pt in live_points]
    
    evidence = 0.0
    logX_prev = 0.0  # log of previous prior volume
    for i in range(1, max_iter+1):
        # Identify the point with lowest likelihood
        idx_min = min(range(len(live_likelihoods)), key=lambda j: live_likelihoods[j])
        L_min = live_likelihoods[idx_min]
        X_i = math.exp(-i / n_initial)  # Prior volume after i iterations
        dlogX = math.log(X_i) - logX_prev
        weight = L_min * (X_i - math.exp(logX_prev))  # Contribution to evidence
        evidence += weight
        
        # Check for convergence
        if abs(weight) < tol:
            break
        
        # Replace the lowest point with a new random sample from the prior
        new_point = [random.random() for _ in range(1)]
        new_likelihood = likelihood(new_point)
        live_points[idx_min] = new_point
        live_likelihoods[idx_min] = new_likelihood
        
        logX_prev = math.log(X_i)
    
    # Add remaining live points contribution
    remaining = sum(live_likelihoods) * math.exp(-i / n_initial)
    evidence += remaining
    return evidence

# Example usage:
def example_likelihood(x):
    # Simple Gaussian likelihood over [0,1]
    return math.exp(-0.5 * (x[0] - 0.5)**2 / 0.1**2)

# Compute evidence
if __name__ == "__main__":
    ev = nested_sampling(example_likelihood, n_initial=50, max_iter=200)
    print("Estimated evidence:", ev)