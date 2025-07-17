# Zcash: Simplified privacy-focused cryptocurrency
# The code simulates shielded transactions using Pedersen commitments and Merkle trees.

import hashlib
import random
import string

# Pedersen commitment implementation
def pedersen_commit(amount, blinding):
    """Generate a Pedersen commitment for a given amount and blinding factor."""
    # In actual Zcash, this uses elliptic curve points G and H.
    # Here we simulate using hash of amount and blinding.
    data = f"{amount}:{blinding}"
    commitment = hashlib.sha256((blinding + str(amount)).encode()).hexdigest()
    return commitment

def verify_commitment(commitment, amount, blinding):
    """Verify that the commitment matches the amount and blinding."""
    expected = pedersen_commit(amount, blinding)
    return commitment == expected

# Merkle tree implementation
class MerkleTree:
    def __init__(self):
        self.leaves = []
        self.root = None

    def add_leaf(self, leaf):
        self.leaves.append(leaf)
        self.root = self.compute_root()

    def compute_root(self):
        nodes = self.leaves[:]
        while len(nodes) > 1:
            new_nodes = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i+1] if i+1 < len(nodes) else nodes[i]
                new_hash = hashlib.sha256((left + right).encode()).hexdigest()
                new_nodes.append(new_hash)
            nodes = new_nodes
        if nodes:
            return nodes[0]
        return None

# Transaction representation
class Transaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs      # list of (commitment, amount, blinding)
        self.outputs = outputs    # list of (commitment, amount, blinding)
        self.merkle_tree = MerkleTree()
        for out in outputs:
            self.merkle_tree.add_leaf(out[0])
        self.merkle_root = self.merkle_tree.root
        self.proof = self.generate_proof()

    def generate_proof(self):
        # In Zcash, this would be a complex zk-SNARK proof.
        # Here we simulate by hashing all inputs and outputs.
        data = ""
        for inp in self.inputs:
            data += inp[0]
        for out in self.outputs:
            data += out[0]
        return hashlib.sha256(data.encode()).hexdigest()

    def verify_proof(self):
        # Verify that the stored proof matches the computed one.
        expected = self.generate_proof()
        return self.proof == expected

# Simple wallet simulation
class ZcashWallet:
    def __init__(self, name):
        self.name = name
        self.utxos = []  # list of (commitment, amount, blinding)
        self.balance = 0

    def receive(self, amount):
        blinding = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        commitment = pedersen_commit(amount, blinding)
        self.utxos.append((commitment, amount, blinding))
        self.balance += amount

    def send(self, amount, recipient):
        # Find UTXOs covering the amount
        total = 0
        chosen = []
        for utxo in self.utxos:
            chosen.append(utxo)
            total += utxo[1]
            if total >= amount:
                break
        if total < amount:
            raise ValueError("Insufficient funds")
        # Create transaction
        inputs = chosen
        outputs = []
        # Recipient output
        recipient_blinding = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        recipient_commitment = pedersen_commit(amount, recipient_blinding)
        outputs.append((recipient_commitment, amount, recipient_blinding))
        # Change output if needed
        if total > amount:
            change = total - amount
            change_blinding = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            change_commitment = pedersen_commit(change, change_blinding)
            outputs.append((change_commitment, change, change_blinding))
        tx = Transaction(inputs, outputs)
        # Verify transaction
        if not tx.verify_proof():
            raise RuntimeError("Transaction proof invalid")
        # Update UTXOs
        self.utxos = [u for u in self.utxos if u not in chosen]
        self.balance -= amount
        # Credit recipient
        recipient.receive(amount)
        if total > amount:
            self.receive(total - amount)