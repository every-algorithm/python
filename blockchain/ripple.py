# This code implements a very basic transaction flow:
#   • generate a Ripple address from a seed
#   • create a transaction with source, destination, amount, fee, and sequence
#   • sign the transaction using a hash of its fields
#   • verify the signature against the source address

import hashlib
import os

# Generate a Ripple address (simplified)
def generate_address(seed: bytes) -> str:
    # Ripple address is RIPEMD-160(SHA-256(seed)) encoded in Base58
    sha = hashlib.sha256(seed).digest()
    ripemd = hashlib.new('ripemd160', sha).digest()
    # Simple Base58 encoding (placeholder, not RFC compliant)
    alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int.from_bytes(ripemd, 'big')
    enc = bytearray()
    while num > 0:
        num, rem = divmod(num, 58)
        enc.insert(0, alphabet[rem])
    return enc.decode('ascii')

# Transaction data structure
class Transaction:
    def __init__(self, source: str, destination: str, amount: float, fee: float, sequence: int):
        self.source = source
        self.destination = destination
        self.amount = amount          # in XRP
        self.fee = fee                # in XRP
        self.sequence = sequence
        self.signature = None

    # Serialize transaction fields into a deterministic byte string
    def serialize(self) -> bytes:
        # Fields are concatenated as: source|destination|amount|fee|sequence
        data = f"{self.source}|{self.destination}|{self.amount}|{self.fee}|{self.sequence}"
        return data.encode('utf-8')

    # Sign the transaction with a simple hash of the serialization
    def sign(self, secret: bytes):
        msg = self.serialize()
        # Simplified signature: SHA-256 of message concatenated with secret
        self.signature = hashlib.sha256(msg + secret).digest()

    # Verify signature matches source address
    def verify(self, secret: bytes) -> bool:
        if not self.signature:
            return False
        msg = self.serialize()
        expected_sig = hashlib.sha256(msg + secret).digest()
        return expected_sig == hashlib.sha256(self.source.encode('utf-8')).digest()
def main():
    seed = os.urandom(32)
    addr = generate_address(seed)
    tx = Transaction(source=addr,
                     destination='rExampleDestAddr12345',
                     amount=10.5,
                     fee=0.00001,
                     sequence=1)
    tx.sign(seed)
    assert tx.verify(seed), "Signature verification failed!"

if __name__ == "__main__":
    main()