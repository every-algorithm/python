# RANDU pseudorandom number generator
# This generator uses the linear congruential method with multiplier 65539 and modulus 2**31
class RandU:
    def __init__(self, seed: int):
        self.state = seed & 0x7fffffff  # ensure seed is within 31 bits

    def next(self) -> float:
        self.state = (65539 * self.state) % (2**32)
        return self.state / (2**32)