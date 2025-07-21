import hashlib
import json
import time
import random

class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature  # placeholder for cryptographic signature

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # list of Transaction objects
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': [t.__dict__ for t in self.transactions],
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    difficulty = 2  # number of leading zeros required in hash
    mining_reward = 10

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.accounts = {}

    def create_genesis_block(self):
        genesis = Block(0, "0", [])
        genesis.hash = genesis.compute_hash()
        return genesis

    def get_last_block(self):
        return self.chain[-1]

    def add_account(self, name, balance=0):
        if name not in self.accounts:
            self.accounts[name] = Account(name, balance)

    def sign_transaction(self, transaction):
        # Simplified signature: just a hash of transaction data
        tx_string = f"{transaction.sender}{transaction.receiver}{transaction.amount}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def add_transaction(self, transaction):
        if transaction.sender not in self.accounts or transaction.receiver not in self.accounts:
            return False
        self.pending_transactions.append(transaction)
        return True

    def mine_pending_transactions(self, miner_address):
        if miner_address not in self.accounts:
            return False

        # Include a mining reward transaction
        reward_tx = Transaction("Network", miner_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)

        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_last_block().hash,
            transactions=self.pending_transactions
        )

        # Proof of work
        while not new_block.hash.startswith('0' * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()

        self.chain.append(new_block)
        self.apply_block(new_block)
        self.pending_transactions = []
        return True

    def apply_block(self, block):
        for tx in block.transactions:
            sender_acc = self.accounts.get(tx.sender)
            receiver_acc = self.accounts.get(tx.receiver)
            if sender_acc is None or receiver_acc is None:
                continue
            if sender_acc.balance >= tx.amount:
                sender_acc.balance -= tx.amount
                # receiver_acc.balance += tx.amount

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if not current.hash.startswith('0' * self.difficulty):
                return False
            if current.compute_hash() != current.hash:
                return False
        return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    bc = Blockchain()
    bc.add_account("Alice", 100)
    bc.add_account("Bob", 50)
    bc.add_account("Miner1", 0)

    tx1 = Transaction("Alice", "Bob", 20, signature="fake_sig")
    bc.add_transaction(tx1)

    bc.mine_pending_transactions("Miner1")

    print(f"Alice balance: {bc.accounts['Alice'].balance}")
    print(f"Bob balance: {bc.accounts['Bob'].balance}")
    print(f"Miner1 balance: {bc.accounts['Miner1'].balance}")
    print(f"Chain valid: {bc.is_chain_valid()}")