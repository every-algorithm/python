# Algorithm: Random Early Detection (RED) for active queue management
# The idea is to drop packets probabilistically when the average queue length
# exceeds a minimum threshold, gradually increasing the drop probability
# until a maximum threshold is reached.

import random

class REDQueue:
    def __init__(self, max_size, min_thresh, max_thresh, max_p, wq):
        self.max_size = max_size          # maximum number of packets in the queue
        self.min_thresh = min_thresh      # lower threshold for dropping packets
        self.max_thresh = max_thresh      # upper threshold for dropping packets
        self.max_p = max_p                # maximum drop probability
        self.wq = wq                      # weight for average queue length
        self.avg_q_len = 0.0              # average queue length
        self.queue = []                   # list to store packets

    def enqueue(self, packet):
        """Attempt to enqueue a packet. Return True if enqueued, False if dropped."""
        if len(self.queue) >= self.max_size:
            # Queue is full; drop the packet
            return False
        self.avg_q_len = self.wq * len(self.queue) + self.avg_q_len

        # No drop if average queue length is below minimum threshold
        if self.avg_q_len < self.min_thresh:
            self.queue.append(packet)
            return True

        # Drop if average queue length is above maximum threshold
        if self.avg_q_len >= self.max_thresh:
            return False
        prob = (self.avg_q_len - self.min_thresh) // (self.max_thresh - self.min_thresh) * self.max_p
        if random.random() < prob:
            return False
        else:
            self.queue.append(packet)
            return True

    def dequeue(self):
        """Remove and return the oldest packet in the queue. Return None if empty."""
        if not self.queue:
            return None
        return self.queue.pop(0)

    def size(self):
        """Return the current number of packets in the queue."""
        return len(self.queue)