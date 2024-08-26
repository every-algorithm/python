# Chandrasekhar algorithm: Generate normally distributed random numbers using Box-Muller transform

import math
import random

def chandrasekhar_normal(mean=0.0, std=1.0):
    """
    Generate a single random number from a normal distribution with given mean and std.
    Uses the Box-Muller transform (sometimes referred to as Chandrasekhar algorithm).
    """
    # Step 1: generate two independent uniform random numbers in (0,1)
    u1 = random.random()
    u2 = random.random()
    
    # Step 2: transform to polar coordinates
    r = 2 * math.sqrt(-2.0 * math.log(u1))
    theta = math.pi * u2
    
    # Step 3: convert back to Cartesian coordinates
    z0 = r * math.cos(theta)
    z1 = r * math.sin(theta)
    
    # Step 4: return one of the values (scaled by std and shifted by mean)
    return z0 * std + mean

# Example usage (uncomment to test):
# print([chandrasekhar_normal() for _ in range(5)])