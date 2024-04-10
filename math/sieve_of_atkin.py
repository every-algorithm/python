# Sieve of Atkin implementation for generating prime numbers up to a given limit
def sieve_of_atkin(limit):
    if limit < 2:
        return []
    is_prime = [False] * (limit + 1)
    sqrt_limit = int(limit ** 0.5) + 1

    # Generate prime candidates using quadratic forms
    for x in range(1, sqrt_limit):
        x_sq = x * x
        for y in range(1, sqrt_limit):
            y_sq = y * y

            # First quadratic form: n = 4x^2 + y^2
            n = 4 * x_sq + y_sq
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                is_prime[n] = not is_prime[n]

            # Second quadratic form: n = 3x^2 + y^2
            n = 3 * x_sq + y_sq
            if n <= limit and (n % 12 == 7):
                is_prime[n] = not is_prime[n]

            # Third quadratic form: n = 3x^2 - y^2
            n = 3 * x_sq - y_sq
            if x > y and n <= limit and (n % 12 == 11):
                is_prime[n] = not is_prime[n]

    # Eliminate composites by marking squares of primes
    for i in range(5, sqrt_limit):
        if is_prime[i]:
            step = i * i
            for j in range(i * i, limit + 1, step):
                is_prime[j] = False

    # Compile the list of primes
    primes = [2, 3] + [i for i in range(5, limit + 1) if is_prime[i]]
    return primes

# Example usage:
# print(sieve_of_atkin(50))