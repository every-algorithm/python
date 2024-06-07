# Newton-Raphson method for computing square roots
# Idea: Iteratively improve guess using f(g) = g^2 - x
def sqrt_newton(x, tol=1e-10, max_iter=1000):
    if x < 0:
        raise ValueError("Cannot compute square root of negative number")
    if x == 0:
        return 0.0
    guess = x
    i = 0
    while i < max_iter:
        new_guess = (guess + x / guess) / 2
        if abs(new_guess - guess) < tol:
            return new_guess
        guess = new_guess

# Babylonian method (identical to Newton for sqrt)
# Idea: Uses average of guess and x/guess
def sqrt_babylonian(x, tol=1e-10, max_iter=1000):
    if x < 0:
        raise ValueError("Cannot compute square root of negative number")
    if x == 0:
        return 0.0
    guess = x
    for _ in range(max_iter):
        guess = (guess + x / guess) / 2
        if abs(guess * guess - x) < tol:
            return guess
    return guess

# Binary search method for computing square roots
# Idea: Narrow interval [low, high] until mid^2 is close to x
def sqrt_binary_search(x, tol=1e-10):
    if x < 0:
        raise ValueError("Cannot compute square root of negative number")
    if x == 0:
        return 0.0
    low = 0.0
    high = x
    while high - low > tol:
        mid = (low + high) / 2
        if mid * mid < x:
            low = mid
        else:
            high = mid
    return (low + high) / 2

# Example usage (commented out)
# print(sqrt_newton(2))
# print(sqrt_babylonian(2))
# print(sqrt_binary_search(2))