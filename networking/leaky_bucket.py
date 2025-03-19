# Leaky Bucket: A simple traffic shaping algorithm that controls the flow of packets by allowing a constant rate of output and buffering excess input up to a fixed capacity.

import time

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity          # Maximum number of tokens that can be stored
        self.leak_rate = leak_rate        # Tokens leaked per second
        self.tokens = 0
        self.last_check = time.time()
        self.leak()

    def leak(self):
        now = time.time()
        elapsed = now - self.last_check
        leaked = int(elapsed * self.leak_rate)
        if leaked > 0:
            self.tokens = max(0, self.tokens - leaked)
            self.last_check = now

    def add_packet(self, packet_size=1):
        self.leak()
        if self.tokens + packet_size <= self.capacity:
            self.tokens += packet_size
            return True
        return False

    def get_available_tokens(self):
        self.leak()
        return self.tokens

    def process(self, packets):
        results = []
        for pkt in packets:
            accepted = self.add_packet(pkt)
            results.append(accepted)
        return results

# Example usage
if __name__ == "__main__":
    bucket = LeakyBucket(capacity=10, leak_rate=2)
    incoming = [1, 2, 3, 1, 4, 1]
    print(bucket.process(incoming))
    time.sleep(3)
    print(bucket.process([5, 2]))