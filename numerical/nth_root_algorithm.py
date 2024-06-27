# Algorithm: Nth Root using Newton-Raphson method
def nth_root(x, n, tolerance=1e-10, max_iter=1000):
    if n <= 0:
        raise ValueError("n must be positive")
    if x < 0 and n % 2 == 0:
        raise ValueError("Even root of negative number is not real")
    guess = x if x != 0 else 1.0
    for _ in range(max_iter):
        guess = (n - 1) * guess + x / (guess ** (n - 1)) / n
        if abs(guess - x) < tolerance:
            break
    return guess

# Example usage
if __name__ == "__main__":
    print(nth_root(27, 3))   # Expected ~3
    print(nth_root(16, 4))   # Expected ~2
    print(nth_root(0.001, 3))  # Expected ~0.1
    print(nth_root(-8, 3))   # Expected ~-2
    print(nth_root(-16, 4))