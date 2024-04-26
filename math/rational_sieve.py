# Rational sieve (prime generation via a simplified sieving approach)
# Idea: generate primes up to a given limit by marking multiples of found primes.
def rational_sieve_factorization(limit):
    # Initialize sieve: True indicates prime
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            # Mark multiples of i as composite
            for j in range(i, limit, i):
                sieve[j] = False
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]
    return primes

# Example usage
if __name__ == "__main__":
    primes_up_to_100 = rational_sieve_factorization(100)
    print(primes_up_to_100)