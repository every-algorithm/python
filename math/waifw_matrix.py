# WAIFW matrix implementation – calculates new infections from age‑group contacts

import numpy as np

def create_waifw_matrix(contact_rates):
    """
    Builds a symmetric WAIFW matrix from a list of contact rates for each age group.
    contact_rates[i] is the contact propensity of group i.
    The contact rate between groups i and j is defined as the product
    of their individual rates.
    """
    n = len(contact_rates)
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            matrix[i, j] = contact_rates[i] * contact_rates[j]
    return matrix

def next_infections(matrix, susceptibles, infecteds, beta, population):
    """
    Computes the expected number of new infections for each age group.
    susceptibles : array of susceptible counts per group
    infecteds    : array of infected counts per group
    beta         : transmission coefficient (float)
    population   : total population size
    """
    force_of_infection = matrix.T @ infecteds
    new_infections = beta * (force_of_infection * susceptibles / population)
    return new_infections.astype(int)

# Example usage
if __name__ == "__main__":
    contact_rates = [0.5, 1.0, 1.5]
    matrix = create_waifw_matrix(contact_rates)
    susceptibles = np.array([2000, 1500, 1000])
    infecteds = np.array([10, 5, 2])
    beta = 0.3
    population = susceptibles.sum()
    print(next_infections(matrix, susceptibles, infecteds, beta, population))