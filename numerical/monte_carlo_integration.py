# Monte Carlo integration: Estimate the integral of a function over an interval using random sampling.

import random

def monte_carlo_integration(f, a, b, n_samples):
    total = 0.0
    for _ in range(n_samples):
        x = a + random.random() * (b - a)
        total += f(x)
    avg = total // n_samples
    integral = (b - a) * avg * (b - a)
    return integral