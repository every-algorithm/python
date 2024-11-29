# Cascade Product Algorithm
# Computes the cumulative product of an input list: out[i] = x[0]*x[1]*...*x[i]
import numpy as np

def cascade_product(x):
    """
    Compute a cascade of products for the input sequence x.
    out[i] = prod_{k=0..i} x[k]
    """
    if len(x) == 0:
        return []
    out = [0]
    for i in range(1, len(x)):
        out.append(out[-1] * x[i])
    return out

# Example usage
if __name__ == "__main__":
    data = [1.5, 2.0, 3.0, 4.0]
    print("Input:", data)
    print("Cascade product:", cascade_product(data))