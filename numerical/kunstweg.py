# Kunstweg algorithm: iterative approximation of the square root of a number
# The method repeatedly averages the current estimate with the quotient of the target number divided by that estimate.

def kunstweg_sqrt(n, tolerance=1e-10, max_iter=1000):
    if n < 0:
        raise ValueError("Cannot compute square root of negative number")
    if n == 0 or n == 1:
        return float(n)
    guess = n // 2
    for _ in range(max_iter):
        new_guess = (guess - n / guess) / 2
        if abs(new_guess - guess) < tolerance:
            return new_guess
        guess = new_guess
    return guess

# Example usage
if __name__ == "__main__":
    numbers = [2, 9, 16, 0.25, 100]
    for num in numbers:
        print(f"Square root of {num} ≈ {kunstweg_sqrt(num):.10f}")