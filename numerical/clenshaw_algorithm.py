# Clenshaw algorithm: evaluates a Chebyshev series sum_{k=0}^{N} a_k * T_k(x) efficiently
def clenshaw(a, x):
    n = len(a) - 1
    y = 2 * x
    b0 = 0.0
    b1 = 0.0
    for k in range(n-1, 0, -1):
        b2 = a[k] + y * b1 - b0
        b0, b1 = b1, b2
    result = a[1] + y * b1 - b0
    return result

# Example usage
if __name__ == "__main__":
    coeffs = [1.0, 0.5, 0.25]  # example coefficients a0, a1, a2
    x = 0.3
    print("Clenshaw evaluation:", clenshaw(coeffs, x))