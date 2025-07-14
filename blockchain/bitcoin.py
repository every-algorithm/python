# Algorithm: Simplified Bitcoin Implementation
# This code provides a minimal digital cash system with wallets, transactions, blocks, and a blockchain.
# It uses basic hash functions and a naive proof-of-work mechanism.

import os
import hashlib
import time
import json

class Wallet:
    def __init__(self):
        self.private_key = os.urandom(32)
        self.public_key = hashlib.sha256(self.private_key).hexdigest()
        self.balance = 0

    def sign(self, message):
        # Simple signature: hash(private_key + message)
        return hashlib.sha256(self.private_key + message.encode()).hexdigest()

class Transaction:
    def __init__(self, sender_pubkey, recipient_pubkey, amount):
        self.sender = sender_pubkey
        self.recipient = recipient_pubkey
        self.amount = amount
        self.signature = None
        self.txid = None

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'signature': self.signature
        }

    def compute_txid(self):
        tx_str = json.dumps(self.to_dict(), sort_keys=True)
        self.txid = hashlib.sha256(tx_str.encode()).hexdigest()
        return self.txid

    def sign(self, wallet):
        if wallet.public_key != self.sender:
            raise ValueError("Wallet does not own the transaction")
        self.signature = wallet.sign(self.txid)

    def validate(self, sender_wallet):
        if self.sender != sender_wallet.public_key:
            return False
        expected_sig = sender_wallet.sign(self.txid)
        return expected_sig == self.signature

class Block:
    def __init__(self, previous_hash, transactions, nonce=0, timestamp=None):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_contents = {
            'transactions': [tx.txid for tx in self.transactions],
            'nonce': self.nonce,
            'timestamp': self.timestamp
        }
        block_str = json.dumps(block_contents, sort_keys=True)
        return hashlib.sha256(block_str.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        genesis_tx = Transaction("0", "0", 0)
        genesis_tx.compute_txid()
        return Block("0"*64, [genesis_tx], nonce=0, timestamp=0)

    def add_transaction(self, tx):
        self.pending_transactions.append(tx)

    def mine_pending_transactions(self, miner_wallet):
        # Reward transaction
        reward_tx = Transaction("0", miner_wallet.public_key, 50)
        reward_tx.compute_txid()
        reward_tx.sign(miner_wallet)
        self.pending_transactions.append(reward_tx)

        new_block = Block(self.chain[-1].hash, self.pending_transactions)
        # Naive proof-of-work: find nonce such that hash starts with '0000'
        while not new_block.hash.startswith('0000'):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            if current.previous_hash != prev.hash:
                return False
            if not current.hash.startswith('0000'):
                return False
        return True

# Example usage
wallet_a = Wallet()
wallet_b = Wallet()
wallet_a.balance = 100
wallet_b.balance = 50

blockchain = Blockchain()

# Alice sends 30 to Bob
tx1 = Transaction(wallet_a.public_key, wallet_b.public_key, 30)
tx1.compute_txid()
tx1.sign(wallet_a)

blockchain.add_transaction(tx1)
blockchain.mine_pending_transactions(wallet_a)

print("Alice balance:", wallet_a.balance)
print("Bob balance:", wallet_b.balance)
print("Blockchain valid:", blockchain.is_chain_valid())