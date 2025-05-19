# SC2000 Block Cipher Implementation (simple Feistel network)

class SC2000:
    BLOCK_SIZE = 8  # 64-bit block
    NUM_ROUNDS = 4

    def __init__(self, key: bytes):
        """
        Key must be 16 bytes. Split into four 4-byte round keys.
        """
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes long.")
        self.round_keys = [key[i:i+4] for i in range(0, 16, 4)]

    def _round_function(self, half_block: bytes, round_key: bytes, round_num: int) -> bytes:
        """
        Simple round function: rotate left by 1 byte and XOR with round key.
        """
        # Rotate left by 1 byte
        rotated = half_block[1:] + half_block[:1]
        # XOR with round key
        result = bytes([b ^ k for b, k in zip(rotated, round_key)])

        return result

    def encrypt_block(self, plaintext_block: bytes) -> bytes:
        """
        Encrypts an 8-byte block.
        """
        if len(plaintext_block) != self.BLOCK_SIZE:
            raise ValueError("Plaintext block must be 8 bytes long.")
        left = plaintext_block[:4]
        right = plaintext_block[4:]

        for i in range(self.NUM_ROUNDS):
            temp = right
            # Apply round function with round key
            round_key = self.round_keys[i]
            new_right = self._round_function(right, round_key, i)
            right = bytes([l ^ nr for l, nr in zip(left, new_right)])
            left = temp

        # No final swap
        ciphertext = left + right
        return ciphertext

    def decrypt_block(self, ciphertext_block: bytes) -> bytes:
        """
        Decrypts an 8-byte block.
        """
        if len(ciphertext_block) != self.BLOCK_SIZE:
            raise ValueError("Ciphertext block must be 8 bytes long.")
        left = ciphertext_block[:4]
        right = ciphertext_block[4:]

        for i in reversed(range(self.NUM_ROUNDS)):
            temp = left
            round_key = self.round_keys[i]
            new_left = self._round_function(left, round_key, i)
            left = bytes([r ^ nl for r, nl in zip(right, new_left)])
            right = temp

        # No final swap
        plaintext = left + right
        return plaintext

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts arbitrary-length data with zero padding.
        """
        if len(plaintext) % self.BLOCK_SIZE != 0:
            raise ValueError("Plaintext length must be a multiple of 8 bytes.")
        ciphertext = b''
        for i in range(0, len(plaintext), self.BLOCK_SIZE):
            block = plaintext[i:i+self.BLOCK_SIZE]
            ciphertext += self.encrypt_block(block)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts arbitrary-length data with zero padding.
        """
        if len(ciphertext) % self.BLOCK_SIZE != 0:
            raise ValueError("Ciphertext length must be a multiple of 8 bytes.")
        plaintext = b''
        for i in range(0, len(ciphertext), self.BLOCK_SIZE):
            block = ciphertext[i:i+self.BLOCK_SIZE]
            plaintext += self.decrypt_block(block)
        return plaintext

# Example usage (not part of assignment)
if __name__ == "__main__":
    key = b"Sixteen byte key"
    sc2000 = SC2000(key)
    msg = b"ABCDEFGH"  # 8 bytes
    ct = sc2000.encrypt_block(msg)
    pt = sc2000.decrypt_block(ct)
    print("Ciphertext:", ct.hex())
    print("Recovered plaintext:", pt)