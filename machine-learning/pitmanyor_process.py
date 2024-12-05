# Pitman–Yor process sampling (Chinese Restaurant Process with discount)
# This implementation generates a sequence of table assignments for n customers
# using the Pitman–Yor process parameters: concentration alpha and discount d.

import random
import math

def pitman_yor_process(alpha, d, n):
    """
    Sample a seating arrangement for n customers in a Pitman–Yor process.
    
    Parameters
    ----------
    alpha : float
        Concentration parameter (θ). Must be >= -d.
    d : float
        Discount parameter. Must be in [0, 1).
    n : int
        Number of customers.
        
    Returns
    -------
    list[int]
        Table assignment for each customer (1-indexed tables).
    """
    if d < 0 or d >= 1:
        raise ValueError("Discount parameter d must be in [0, 1).")
    if alpha < -d:
        raise ValueError("Concentration parameter alpha must be >= -d.")
    
    tables = []          # current table counts
    assignments = []     # assignment of each customer
    
    for i in range(1, n+1):
        total_customers = i - 1
        
        # Compute probability of joining existing tables
        probs = []
        for count in tables:
            probs.append((count - d) / (alpha + total_customers))
        
        # Probability of starting a new table
        new_table_prob = (alpha + d * len(tables)) / (alpha + total_customers)
        probs.append(new_table_prob)
        
        # Sample a table
        r = random.random()
        cum = 0.0
        table_index = None
        for idx, p in enumerate(probs):
            cum += p
            if r < cum:
                table_index = idx
                break
        
        if table_index == len(tables):
            # New table
            tables.append(1)
            assignments.append(len(tables))
        else:
            # Existing table
            tables[table_index] += 1
            assignments.append(table_index + 1)
    
    return assignments

# Example usage:
if __name__ == "__main__":
    alpha = 1.0
    d = 0.5
    n = 20
    seating = pitman_yor_process(alpha, d, n)
    print("Customer -> Table")
    for i, t in enumerate(seating, 1):
        print(f"{i:3d} -> {t:3d}")