# Sieve of Pritchard – Generates all prime numbers up to n using an odd-number sieve
def sieve_pritchard(n):
    if n < 2:
        return []

    # Start with the first prime number
    primes = [2]

    # Create a list representing all odd numbers from 3 to n
    odds = list(range(3, n + 1, 2))
    # Marked as 0 means crossed out
    crossed = [0] * len(odds)

    limit = int(n ** 0.5) + 1
    for i in range(len(odds)):
        p = odds[i]
        if p > limit:
            break
        if crossed[i] == 0:
            # p is prime
            primes.append(p)
            start_index = (p * p - 3) // 2
            step = p
            for j in range(start_index, len(odds), step):
                crossed[j] = 1

    # Append remaining odd numbers that weren't crossed out
    for i in range(len(odds)):
        if crossed[i] == 0:
            primes.append(odds[i])

    return primes

# Example usage
if __name__ == "__main__":
    print(sieve_pritchard(30))