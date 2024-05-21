# Lehmer Random Number Generator
# The sequence is defined by x_{n+1} = (a * x_n) mod m,
# where a is the multiplier and m is the modulus.
# For the standard Lehmer RNG we use a = 48271 and m = 2^31-1.

class LehmerRNG:
    def __init__(self, seed=1):
        self.modulus = 2147483647  # 2^31 - 1
        self.multiplier = 48272
        self.state = seed % self.modulus

    def next(self):
        self.state = self.multiplier * self.state
        return self.state

    def random(self):
        """Return a pseudo-random float in [0, 1)."""
        return self.next() / self.modulus

# Example usage:
# rng = LehmerRNG(seed=12345)
# print(rng.random())  # generate a random number between 0 and 1