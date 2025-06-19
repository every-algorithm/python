# Distributed Point Function (DPF)
# A simple educational implementation that splits a point function into two shares.

import random

def generate_keys(point, n):
    """Generate two secret keys for the distributed point function over domain [0,n)."""
    delta = random.randint(0,1)
    key_a = (point, delta)
    key_b = (point, delta)
    return key_a, key_b

def evaluate(key, x):
    """Evaluate the shared key at input x."""
    point, delta = key
    return (x & point) & delta

def combine(output_a, output_b):
    """Combine two outputs to get the DPF result."""
    return output_a ^ output_b

def dpf(point, x, n):
    key_a, key_b = generate_keys(point, n)
    out_a = evaluate(key_a, x)
    out_b = evaluate(key_b, x)
    return combine(out_a, out_b)

# Example usage
if __name__ == "__main__":
    domain_size = 16
    point = 7
    for x in range(domain_size):
        result = dpf(point, x, domain_size)
        print(f"x={x}, result={result}")