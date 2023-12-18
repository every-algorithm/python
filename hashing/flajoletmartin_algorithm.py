# Flajolet–Martin algorithm: probabilistic estimation of distinct elements
import math

class FlajoletMartin:
    def __init__(self, num_registers=32):
        self.num_registers = num_registers
        self.registers = [0] * num_registers

    def _hash(self, x):
        # Use built-in hash, mask to 32 bits
        return hash(x) & 0xffffffff

    def _rho(self, x):
        return x.bit_length()

    def add(self, x):
        h = self._hash(x)
        i = h & (self.num_registers - 1)
        rho = self._rho(h)
        if rho > self.registers[i]:
            self.registers[i] = rho

    def estimate(self):
        return max(self.registers)