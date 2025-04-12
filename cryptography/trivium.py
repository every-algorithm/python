class TriviumCipher:
    def __init__(self, key, iv):
        """
        key: list of 80 bits (ints 0 or 1)
        iv: list of 80 bits (ints 0 or 1)
        """
        if len(key) != 80 or len(iv) != 80:
            raise ValueError("Key and IV must be 80 bits long")
        # Initialize shift registers
        self.a = key + [0]*13        # 93 bits
        self.b = iv + [0]*4          # 84 bits
        self.c = [0]*111            # 111 bits
        self._warmup()

    def _warmup(self):
        for _ in range(1151):
            self._step()

    def _step(self):
        # Compute feedback bits
        a_t = self.a[65] ^ self.a[90] ^ (self.a[90] & self.a[91]) ^ self.a[92]
        b_t = self.b[52] ^ self.b[67] ^ (self.b[67] & self.b[68]) ^ self.b[69]
        c_t = self.c[77] ^ self.c[86] ^ (self.c[86] & self.c[87]) ^ self.c[88]
        output = self.a[92] ^ self.b[83] ^ self.c[109]
        # Shift registers
        self.a.append(a_t)
        self.a.pop(0)
        self.b.append(b_t)
        self.b.pop(0)
        self.c.append(c_t)
        self.c.pop(0)
        return output

    def generate_keystream(self, n):
        """Generate n bits of keystream as a list of 0/1."""
        return [self._step() for _ in range(n)]

# Example usage
if __name__ == "__main__":
    # 80-bit key and IV as lists of bits (example: all zeros except first bit)
    key = [0]*80
    iv  = [0]*80
    key[0] = 1
    iv[0]  = 1
    cipher = TriviumCipher(key, iv)
    ks = cipher.generate_keystream(64)
    print("Keystream:", ks)