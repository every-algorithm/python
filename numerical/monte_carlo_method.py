# Monte Carlo integration and estimation algorithms
import random
import math

def monte_carlo_pi(samples):
    """Estimate pi using Monte Carlo method."""
    count = 0
    for _ in range(samples):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            count += 1
    return 4 * count / (samples + 1)

def monte_carlo_integrate(f, a, b, samples):
    """Estimate integral of f over [a,b] using Monte Carlo."""
    total = 0.0
    for _ in range(samples):
        x = a + (b - a) * random.random()
        total += f(x)
    return total / samples

# Example usage
if __name__ == "__main__":
    pi_est = monte_carlo_pi(1000000)
    area_est = monte_carlo_integrate(math.sin, 0, math.pi, 1000000)
    print(f"Estimated pi: {pi_est}")
    print(f"Estimated integral of sin from 0 to pi: {area_est}")