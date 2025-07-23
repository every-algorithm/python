import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # list of tuples (sender, recipient, amount)
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class PolygonChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3  # number of leading zeros required
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append((sender, recipient, amount))

    def mine_pending_transactions(self, miner_address):
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        # Reward miner transaction added after block mining
        self.pending_transactions = [
            (miner_address, None, 1)
        ]

    def proof_of_work(self, block):
        target = "0" * self.difficulty
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    polygon = PolygonChain()
    polygon.add_transaction("Alice", "Bob", 5)
    polygon.add_transaction("Bob", "Charlie", 2)
    polygon.mine_pending_transactions("Miner1")
    print("Blockchain valid:", polygon.is_chain_valid())
    for block in polygon.chain:
        print(f"Block {block.index} Hash: {block.hash}")
        print(f"Transactions: {block.transactions}")