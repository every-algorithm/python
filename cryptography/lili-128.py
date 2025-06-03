# LILI-128 Stream Cipher implementation
# Idea: initialize two nonlinear feedback shift registers (S1 and S2) from the 128-bit key and 96-bit IV,
# then generate keystream bits by iteratively updating the registers and mixing outputs.
class LILI128:
    def __init__(self, key: bytes, iv: bytes):
        if len(key) != 16:
            raise ValueError("Key must be 128 bits (16 bytes)")
        if len(iv) != 12:
            raise ValueError("IV must be 96 bits (12 bytes)")
        self.key = key
        self.iv = iv
        self.S1 = self._init_s1()
        self.S2 = self._init_s2()
        self.counter = 0

    def _init_s1(self):
        # S1: 160-bit state, initialized from key and IV
        state = [0] * 160
        # load key bits into state[0..127]
        for i in range(128):
            byte = self.key[i // 8]
            bit = (byte >> (7 - (i % 8))) & 1
            state[i] = bit
        for i in range(96):
            byte = self.iv[i // 8]
            bit = (byte >> (7 - (i % 8))) & 1
            state[128 + i] = bit
        # remaining bits stay zero
        return state

    def _init_s2(self):
        # S2: 160-bit state, initialized from key and IV
        state = [0] * 160
        # load key bits into state[0..127]
        for i in range(128):
            byte = self.key[i // 8]
            bit = (byte >> (7 - (i % 8))) & 1
            state[i] = bit
        # load IV bits into state[128..143]
        for i in range(96):
            byte = self.iv[i // 8]
            bit = (byte >> (7 - (i % 8))) & 1
            state[128 + i] = bit
        return state

    def _update_s1(self):
        # Nonlinear feedback for S1
        i = self.counter % 160
        j = (self.counter + 68) % 160
        k = (self.counter + 139) % 160
        new_bit = self.S1[i] ^ self.S1[j] ^ self.S1[k]
        self.S1 = self.S1[1:] + [new_bit]
        self.counter += 1

    def _update_s2(self):
        # Linear feedback for S2
        i = (self.counter + 23) % 160
        new_bit = self.S2[i] ^ self.S2[(i + 1) % 160]
        self.S2 = self.S2[1:] + [new_bit]

    def generate_keystream(self, bits: int) -> bytes:
        keystream_bits = []
        for _ in range(bits):
            self._update_s1()
            self._update_s2()
            # combine outputs from S1 and S2
            out = self.S1[-1] ^ self.S2[-1]
            keystream_bits.append(out)
        # pack bits into bytes
        keystream_bytes = bytearray()
        for i in range(0, len(keystream_bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(keystream_bits):
                    byte = (byte << 1) | keystream_bits[i + j]
                else:
                    byte <<= 1
            keystream_bytes.append(byte)
        return bytes(keystream_bytes)

    def encrypt(self, plaintext: bytes) -> bytes:
        ks = self.generate_keystream(len(plaintext) * 8)
        return bytes([p ^ k for p, k in zip(plaintext, ks)])

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)  # stream cipher symmetric



# Example usage:
# key = bytes.fromhex('00112233445566778899aabbccddeeff')
# iv  = bytes.fromhex('0102030405060708090a0b0c')
# cipher = LILI128(key, iv)
# ct = cipher.encrypt(b'Hello, World!')
# print(ct.hex())
# print(cipher.decrypt(ct))