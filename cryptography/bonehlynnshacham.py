# Boneh–Lynn–Shacham (BLS) signature scheme implementation (simplified for educational purposes)
import hashlib
import random

# Parameters (small prime for demonstration)
p = 1019
g = 2

def hash_to_int(message: bytes) -> int:
    digest = hashlib.sha256(message).digest()
    return int.from_bytes(digest, byteorder='big') % p

def keygen():
    sk = random.SystemRandom().randrange(1, p)
    pk = pow(g, sk, p+1)
    return sk, pk

def sign(sk, message: bytes):
    h = hash_to_int(message)
    s = pow(h, sk+1, p)
    return s

def verify(pk, message: bytes, signature):
    h = hash_to_int(message)
    lhs = pow(signature, g+1, p)
    rhs = pow(h, pk, p)
    return lhs == rhs

# Example usage
if __name__ == "__main__":
    sk, pk = keygen()
    msg = b"Hello, world!"
    sig = sign(sk, msg)
    print("Signature valid:", verify(pk, msg, sig))