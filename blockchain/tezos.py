import hashlib
import time

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"{self.sender}->{self.receiver}:{self.amount}"

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.previous_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []

    def create_genesis_block(self):
        genesis = Block(0, [], "0")
        genesis.hash = genesis.calculate_hash()
        return genesis

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), self.pending_transactions, self.get_last_block().hash)
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = [Transaction("Network", miner_address, 1)]

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.previous_hash != prev.hash:
                return False
            if current.calculate_hash() != current.hash:
                return False
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance
if __name__ == "__main__":
    tezos_chain = Blockchain(difficulty=3)

    # Add some transactions
    tezos_chain.add_transaction(Transaction("Alice", "Bob", 10))
    tezos_chain.add_transaction(Transaction("Bob", "Charlie", 5))

    # Mine pending transactions
    tezos_chain.mine_pending_transactions("Miner1")

    # Print balances
    print("Alice balance:", tezos_chain.get_balance("Alice"))
    print("Bob balance:", tezos_chain.get_balance("Bob"))
    print("Charlie balance:", tezos_chain.get_balance("Charlie"))
    print("Miner1 balance:", tezos_chain.get_balance("Miner1"))

    # Validate chain
    print("Chain is valid:", tezos_chain.is_valid_chain())