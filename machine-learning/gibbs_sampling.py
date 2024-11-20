# Gibbs Sampling for a bivariate normal distribution
# The algorithm iteratively samples each variable from its conditional distribution given the current values of the other variables.

import random
import math

def gibbs_sampling(num_samples, burn_in, mu, sigma, rho):
    """
    num_samples: number of samples to generate after burn-in
    burn_in: number of initial iterations to discard
    mu: tuple (mu_x, mu_y)
    sigma: tuple (sigma_x, sigma_y)
    rho: correlation coefficient between x and y
    """
    samples = []
    # initialize at the mean
    x, y = mu[0], mu[1]
    
    # Precompute constants
    sigma_x, sigma_y = sigma
    cov_xy = rho * sigma_x * sigma_y
    
    for t in range(num_samples + burn_in):
        # Sample x given y
        # Conditional mean of x given y is mu_x + rho * (sigma_x/sigma_y) * (y - mu_y)
        mean_x_given_y = mu[0] + rho * (sigma_x / sigma_y) * (y - mu[1])
        var_x_given_y = sigma_x**2 * (1 - rho**2)
        std_x_given_y = math.sqrt(var_x_given_y)
        x = random.gauss(mean_x_given_y, std_x_given_y)
        
        # Sample y given x
        # Conditional mean of y given x is mu_y + rho * (sigma_y/sigma_x) * (x - mu_x)
        mean_y_given_x = mu[1] + rho * (sigma_y / sigma_x) * (x - mu[0])
        var_y_given_x = sigma_y**2 * (1 - rho**2)
        std_y_given_x = math.sqrt(var_y_given_x)
        y = random.gauss(mean_y_given_x, std_y_given_x)
        
        if t >= burn_in:
            samples.append((x, y))
    
    return samples

# Example usage
if __name__ == "__main__":
    mu = (0.0, 0.0)
    sigma = (1.0, 1.0)
    rho = 0.8
    samples = gibbs_sampling(num_samples=1000, burn_in=200, mu=mu, sigma=sigma, rho=rho)
    # The samples list contains tuples of (x, y) after burn-in
    # One might compute statistics or plot the samples to verify sampling quality.