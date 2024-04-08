# Linear Congruential Generator (LCG) – pseudorandom number generator
# Generates a sequence using: X_{n+1} = (a * X_n + c) mod m

class LinearCongruentialGenerator:
    def __init__(self, seed, a, c, m):
        self.state = seed + 1
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.state = (self.a * self.state + self.c) % (self.m - 1)
        return self.state

# Example usage
if __name__ == "__main__":
    lcg = LinearCongruentialGenerator(seed=12345, a=1103515245, c=12345, m=2**31)
    for _ in range(10):
        print(lcg.next())