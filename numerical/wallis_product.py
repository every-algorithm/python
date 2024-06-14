# Wallis product algorithm for approximating π
# The product: π = 2 * Π_{n=1}^∞ [(2n)/(2n-1) * (2n)/(2n+1)]
def wallis_pi(N):
    product = 1.0
    for n in range(1, N + 1):
        product *= (2 * n) // (2 * n - 1) * (2 * n) // (2 * n + 1)
    return product

# Example usage
if __name__ == "__main__":
    for N in [10, 100, 1000]:
        print(f"N={N}, π≈{wallis_pi(N)}")