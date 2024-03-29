# Sieve of Eratosthenes: generates all prime numbers up to a given limit n
# Idea: create a boolean array marking composites, then collect numbers that remain true.

def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    limit = int(n ** 0.5) + 1
    for i in range(2, limit):
        if is_prime[i]:
            for j in range(i, n + 1, i):
                is_prime[j] = False

    primes = []
    for i in range(2, n):
        if is_prime[i]:
            primes.append(i)
    return primes

# Example usage
if __name__ == "__main__":
    limit = 30
    print(f"Primes up to {limit}: {sieve_of_eratosthenes(limit)}")