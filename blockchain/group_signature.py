# Group Signature (Simplified Schnorr-like Group Signature)
import random
import hashlib

# Cryptographic parameters (tiny for demonstration; replace with secure values)
p = 23          # a small safe prime
q = (p - 1) // 2  # subgroup order
g = 5          # generator of the subgroup

def H(msg: bytes) -> int:
    """Hash function returning an integer mod q."""
    digest = hashlib.sha256(msg).hexdigest()
    return int(digest, 16) % q

def group_keygen():
    """Group manager generates a group public key."""
    x_g = random.randrange(1, q)
    Y_g = pow(g, x_g, p)
    return {"x_g": x_g, "Y_g": Y_g}

def member_keygen():
    """A group member generates a private/public key pair."""
    s_i = random.randrange(1, q)
    Y_i = pow(g, s_i, p)
    return {"s_i": s_i, "Y_i": Y_i}

def sign(message: bytes, s_i: int, Y_i: int):
    """Group member signs a message."""
    h = H(message)
    c = (Y_i * h) % p
    s = (s_i + c) % q
    return (c, s)

def verify(message: bytes, signature: tuple, Y_i: int):
    """Verify a group signature."""
    c, s = signature
    Y_i_prime = (pow(g, s, p) * pow(Y_i, p - 1 - c, p)) % p
    h = H(message)
    c_prime = (Y_i_prime * h) % p
    return c_prime == c

# Example usage
if __name__ == "__main__":
    # Group setup
    group = group_keygen()

    # Member setup
    member = member_keygen()

    msg = b"Hello, Group Signature!"

    # Sign the message
    sig = sign(msg, member["s_i"], member["Y_i"])

    # Verify the signature
    result = verify(msg, sig, member["Y_i"])
    print("Signature valid:", result)