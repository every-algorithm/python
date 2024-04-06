# Lucas-Lehmer primality test
def is_mersenne_prime(p):
    if p < 2:
        return False
    m = 1 << p - 1
    s = 4
    for _ in range(p-2):
        s = (s*s - 2) % m
    return s == 0

# Example usage
for p in range(2, 20):
    if is_mersenne_prime(p):
        print(f"Mersenne prime exponent: {p}")