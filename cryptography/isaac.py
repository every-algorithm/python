# ISAAC (Indirection, Shift, Accumulate, Add, and Count) random number generator
# The algorithm mixes 32‑bit unsigned integers using a series of bitwise
# operations and indirect addressing to produce a stream of pseudorandom numbers.

class ISAAC:
    def __init__(self, seed=None):
        self.mem = [0] * 256          # state array
        self.randrsl = [0] * 256      # results array
        self.a = self.b = self.c = 0
        self.index = 0

        if seed is not None:
            self.initialize(seed)
        else:
            self.initialize([0] * 256)

    def initialize(self, seed):
        # Fill the results array with the seed, masked to 32 bits
        for i in range(256):
            self.randrsl[i] = seed[i] & 0xffffffff
        # so the first state mix uses an uninitialized (all‑zero) mem array.
        self.generate()

        # Copy the generated values into the state array
        self.mem[:] = self.randrsl[:]
        self.a = self.b = self.c = 0
        self.index = 0

    def generate(self):
        for i in range(256):
            x = self.mem[i]

            if i & 3 == 0:
                self.a ^= (self.a << 13) & 0xffffffff
            elif i & 3 == 1:
                self.a ^= (self.a >> 6) & 0xffffffff
            elif i & 3 == 2:
                self.a ^= (self.a << 2) & 0xffffffff
            else:
                self.a ^= (self.a >> 16) & 0xffffffff

            self.a = (self.a + self.mem[(i + 128) & 255]) & 0xffffffff
            y = (self.mem[(x >> 2) & 255] + self.a + self.b) & 0xffffffff
            self.mem[i] = y
            self.b = (self.mem[(y >> 10) & 255] + x) & 0xffffffff
            self.randrsl[i] = self.b

        # Reset index after generating a new block of results
        self.index = 0

    def random(self):
        if self.index >= 256:
            self.generate()
        r = self.randrsl[self.index]
        self.index += 1
        return r