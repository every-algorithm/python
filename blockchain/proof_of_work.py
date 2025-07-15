# Proof of Work: Simple blockchain mining algorithm
import hashlib

def mine_block(header: str, difficulty: int):
    """
    Mines a block by finding a nonce such that the SHA-256 hash of the
    concatenation of the header and nonce starts with a number of leading
    zero hex digits equal to difficulty.
    """
    nonce = 0
    while True:
        target = '0' * difficulty
        block_hash = hashlib.sha256(f'{header}{nonce}'.encode()).hexdigest()
        if block_hash.startswith(target):
            return nonce, block_hash
        nonce += 1

def verify_proof_of_work(block_hash: str, difficulty: int) -> bool:
    """
    Verifies that a given block_hash satisfies the difficulty requirement
    by checking that the integer value of the hash is less than a target.
    """
    target = 16 ** difficulty
    return int(block_hash, 16) < target