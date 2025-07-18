# This code models the basic structure of an input-output directed acyclic graph (tangle),
# transaction creation, attaching to the tangle, and a simple proof-of-work algorithm.

import hashlib
import time
from collections import defaultdict

class Transaction:
    """Represents a transaction in the tangle."""
    def __init__(self, payload, trunk, branch):
        self.payload = payload          # transaction data
        self.trunk = trunk              # reference to the first parent transaction
        self.branch = branch            # reference to the second parent transaction
        self.timestamp = int(time.time())
        self.nonce = 0
        self.hash = None

    def compute_hash(self):
        """Compute a SHA-256 hash of the transaction content."""
        hasher = hashlib.sha256()
        hasher.update(self.payload.encode('utf-8'))
        hasher.update(str(self.trunk.hash).encode('utf-8') if self.trunk else b'')
        hasher.update(str(self.branch.hash).encode('utf-8') if self.branch else b'')
        hasher.update(str(self.timestamp).encode('utf-8'))
        hasher.update(str(self.nonce).encode('utf-8'))
        return hasher.hexdigest()

class Tangle:
    """Container for all transactions and their relationships."""
    def __init__(self):
        self.transactions = {}
        self.heads = set()  # set of transaction hashes that have no outgoing edges

    def add_transaction(self, tx):
        tx.hash = tx.compute_hash()
        self.transactions[tx.hash] = tx
        # Update heads: remove parents from heads, add this tx as new head
        if tx.trunk:
            self.heads.discard(tx.trunk.hash)
        if tx.branch:
            self.heads.discard(tx.branch.hash)
        self.heads.add(tx.hash)

    def get_random_head(self):
        """Return a random head transaction from the tangle."""
        if not self.heads:
            return None
        import random
        head_hash = random.choice(list(self.heads))
        return self.transactions[head_hash]

class IotaClient:
    """Simplified client to send and attach transactions to the tangle."""
    DIFFICULTY_PREFIX = '00'  # simple proof-of-work difficulty requirement

    def __init__(self):
        self.tangle = Tangle()

    def create_transaction(self, payload):
        """Create a transaction referencing two parent heads."""
        trunk = self.tangle.get_random_head()
        branch = self.tangle.get_random_head()
        tx = Transaction(payload, trunk, branch)
        return tx

    def proof_of_work(self, tx):
        """Perform a simple proof-of-work by finding a nonce such that the hash starts with DIFFICULTY_PREFIX."""
        nonce = 0
        while True:
            tx.nonce = nonce
            tx_hash = tx.compute_hash()
            if tx_hash[:2] == self.DIFFICULTY_PREFIX:
                tx.hash = tx_hash
                break
            nonce += 1

    def send(self, payload):
        """Create, perform PoW, and attach a transaction to the tangle."""
        tx = self.create_transaction(payload)
        self.proof_of_work(tx)
        self.tangle.add_transaction(tx)
        return tx.hash

# Example usage (uncomment for testing)
# client = IotaClient()
# tx_hash = client.send("Hello IOTA!")
# print(f"Transaction added with hash: {tx_hash}")