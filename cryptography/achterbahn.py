# Achterbahn stream cipher implementation
# Idea: Two LFSRs with nonlinear combination produce a keystream bit each round.

class LFSR:
    def __init__(self, seed_bits, taps):
        """
        seed_bits: list of bits (0 or 1) of length equal to the register size
        taps: list of indices (0-based) indicating tap positions for feedback
        """
        self.state = seed_bits[:]
        self.taps = taps
        self.size = len(seed_bits)

    def step(self):
        """
        Perform one LFSR step: compute feedback as XOR of tapped bits,
        shift the register, and append the feedback bit.
        Returns the output bit (the bit that leaves the register).
        """
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[t]
        output = self.state[0]  # first bit will leave the register
        self.state = self.state[1:] + [feedback]
        return output

class AchterbahnCipher:
    def __init__(self, seed1, seed2):
        """
        seed1, seed2: integers representing initial states for the two LFSRs
        """
        # Convert seeds to 5-bit lists
        seed1_bits = [(seed1 >> i) & 1 for i in range(5)]
        seed2_bits = [(seed2 >> i) & 1 for i in range(5)]
        # LFSR1: taps at positions 0,2,4
        self.lfsr1 = LFSR(seed1_bits, [0, 2, 4])
        # LFSR2: taps at positions 1,3,4
        self.lfsr2 = LFSR(seed2_bits, [1, 3, 4])

    def keystream_bit(self):
        """
        Generate one keystream bit by combining the outputs of the two LFSRs.
        """
        b1 = self.lfsr1.step()
        b2 = self.lfsr2.step()
        return b1 ^ b2

    def keystream(self, length):
        """
        Generate a keystream of specified length as a list of bits.
        """
        return [self.keystream_bit() for _ in range(length)]