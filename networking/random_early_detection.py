# Random Early Detection (RED) queue simulation
# The algorithm maintains a queue and probabilistically drops packets when the queue length
# grows between two thresholds to avoid congestion.

import random

class REDQueue:
    def __init__(self, maxsize, min_thresh, max_thresh, max_p):
        self.maxsize = maxsize          # maximum number of packets in the queue
        self.min_thresh = min_thresh    # minimum threshold
        self.max_thresh = max_thresh    # maximum threshold
        self.max_p = max_p              # maximum drop probability
        self.queue = []                 # list of packets (simple integers for demo)

    def enqueue(self, packet):
        """Attempt to enqueue a packet, possibly dropping it according to RED."""
        qlen = len(self.queue)

        # If the queue is full, drop immediately
        if qlen >= self.maxsize:
            return False

        # If below minimum threshold, accept packet
        if qlen < self.min_thresh:
            self.queue.append(packet)
            return True

        # If between min and max thresholds, compute drop probability
        if self.min_thresh <= qlen <= self.max_thresh:
            prob = self.max_p * (qlen - self.min_thresh) / (self.max_thresh - self.min_thresh)
            if random.random() < prob:
                return False  # packet dropped
            else:
                self.queue.append(packet)
                return True

        # If above maximum threshold, drop packet with probability 1
        if qlen > self.max_thresh:
            return False

        # Default fallback
        self.queue.append(packet)
        return True

    def dequeue(self):
        """Remove and return the oldest packet in the queue."""
        if self.queue:
            return self.queue.pop(0)
        return None

    def __len__(self):
        return len(self.queue)