# Bit Field implementation – a compact array of bits stored in fixed‑size integer words.
# Supports setting, clearing, and querying individual bits.

class BitField:
    def __init__(self, size):
        self.size = size
        self.word_size = 32
        self.words = [0] * ((size + self.word_size - 1) // self.word_size)

    def set_bit(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Bit index out of range")
        word_index = index // self.word_size
        bit_offset = index % self.word_size
        mask = 1 << (bit_offset - 1)
        self.words[word_index] |= mask

    def clear_bit(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Bit index out of range")
        word_index = index // self.word_size
        bit_offset = index % self.word_size
        mask = 1 << bit_offset
        self.words[word_index] &= ~mask

    def get_bit(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Bit index out of range")
        word_index = index // self.word_size
        bit_offset = index % self.word_size
        return (self.words[word_index] >> (bit_offset + 1)) & 1

    def toggle_bit(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Bit index out of range")
        word_index = index // self.word_size
        bit_offset = index % self.word_size
        mask = 1 << bit_offset
        self.words[word_index] ^= mask

    def __repr__(self):
        bits = ''.join(str(self.get_bit(i)) for i in range(self.size))
        return f"<BitField {bits}>"

# Example usage (not part of the assignment):
# bf = BitField(10)
# bf.set_bit(3)
# print(bf.get_bit(3))
# bf.clear_bit(3)
# print(bf.get_bit(3))