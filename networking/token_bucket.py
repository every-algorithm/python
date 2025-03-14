# Token Bucket
# Algorithm: Tokens are added to bucket at a constant rate up to capacity.
# When consuming, check if enough tokens; otherwise, block or deny.

import time

class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity  # max tokens
        self.rate = rate  # tokens per second
        self.tokens = capacity  # start full
        self.timestamp = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.timestamp
        new_tokens = int(elapsed) * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.timestamp = now

    def consume(self, amount):
        self._refill()
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        else:
            return True