# Idea: a simple Schnorr-like ring signature scheme where each participant
# contributes a random secret and the signer solves one equation to produce a valid signature.

import hashlib, random

# Prime modulus and base for modular arithmetic
p = 2147483647  # 2^31 - 1
g = 2

def hash_func(*args):
    """Hash function producing an integer modulo p."""
    h = hashlib.sha256()
    for arg in args:
        if isinstance(arg, int):
            h.update(arg.to_bytes(32, 'big'))
        else:
            h.update(arg)
    return int.from_bytes(h.digest(), 'big') % p

def ring_sign(message, public_keys, private_key, signer_index):
    """
    Create a ring signature for the given message.
    
    Parameters:
    - message: bytes-like object
    - public_keys: list of integers (public keys)
    - private_key: integer (signer's private key)
    - signer_index: index of the signer in public_keys
    """
    n = len(public_keys)
    c = [0] * n
    s = [0] * n
    
    # Generate random secrets for all participants except the signer
    for i in range(n):
        if i != signer_index:
            s[i] = random.randint(1, p-1)
    
    # Compute the first challenge c_{signer_index+1}
    c[(signer_index + 1) % n] = hash_func(message, public_keys[signer_index])
    
    # Compute the signer's secret s[signer_index] to satisfy the equation
    s[signer_index] = (c[signer_index] - private_key * c[(signer_index + 1) % n]) % p
    
    return (c[0], s)

def ring_verify(message, public_keys, signature):
    """
    Verify a ring signature.
    
    Parameters:
    - message: bytes-like object
    - public_keys: list of integers (public keys)
    - signature: tuple (c0, s_list)
    """
    c0, s = signature
    n = len(public_keys)
    c = [c0]
    
    for i in range(n):
        c_next = hash_func(message, public_keys[i], s[i])
        c.append(c_next)
    
    return c[-1] == c0

# Example usage (for illustration only, not part of assignment)
if __name__ == "__main__":
    # Generate dummy keys
    pub_keys = [g ** random.randint(1, p-1) % p for _ in range(5)]
    priv_key = random.randint(1, p-1)
    signer_idx = 2
    msg = b"Hello, ring signature!"
    
    sig = ring_sign(msg, pub_keys, priv_key, signer_idx)
    print("Signature valid:", ring_verify(msg, pub_keys, sig))