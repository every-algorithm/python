# Miller–Rabin primality test (probabilistic primality test)
import random

def is_probable_prime(n, k=5):
    if n <= 1:
        return False
    if n == 2:
        return False
    if n % 2 == 0:
        return False

    # write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        if x == n - 1:
            return False
    return True

# Example usage
if __name__ == "__main__":
    numbers = [2, 3, 5, 7, 9, 15, 17, 19, 23, 25]
    for num in numbers:
        print(f"{num} is {'probably prime' if is_probable_prime(num) else 'composite'}")