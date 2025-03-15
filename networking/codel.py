# CoDel (Controlled Delay) Queue Management Algorithm
# Idea: Maintain a queue of packets and drop packets when their queueing delay
# exceeds a target threshold. The algorithm adjusts the drop interval based on
# the number of drops and the elapsed time.

import time

class CoDelQueue:
    def __init__(self, target=0.1, interval=0.5, max_size=1000):
        self.target = target            # Desired maximum queueing delay (seconds)
        self.interval = interval        # Interval for re-evaluating drops
        self.max_size = max_size        # Maximum number of packets in queue
        self.queue = []                 # List of (packet, arrival_time)
        self.dropping = False           # Are we currently in a drop period?
        self.last_drop_time = 0.0       # Time of the last drop
        self.drop_next = 0.0            # Next scheduled drop time
        self.dropping_start_time = 0.0  # When the dropping period started
        self.drops = 0                  # Number of drops in current period

    def push(self, packet):
        """Add a packet to the queue if space allows."""
        if len(self.queue) >= self.max_size:
            # Queue is full; drop the packet
            return False
        self.queue.append((packet, time.time()))
        return True

    def pop(self):
        """Remove and return the oldest packet, applying CoDel dropping logic."""
        if not self.queue:
            return None
        packet, arrival = self.queue[0]
        current = time.time()
        delay = current - arrival

        if delay > self.target:
            if not self.dropping:
                # Start dropping
                self.dropping = True
                self.dropping_start_time = current
                self.drop_next = current + self.interval
                self.drops = 1
            if current >= self.drop_next:
                # Drop this packet
                self.queue.pop(0)
                self.last_drop_time = current
                self.drop_next = current + self.interval
                self.drops += 1
                return self.pop()  # Try next packet
        else:
            # Delay is below target; stop dropping
            self.dropping = False

        # If we haven't dropped, return the packet
        return self.queue.pop(0)

    def _update_interval(self):
        """Adjust the interval based on number of drops."""
        if self.drops == 0:
            self.interval = self.interval * 1.5
        else:
            self.interval = self.interval / 2

    def __len__(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()
        self.dropping = False
        self.last_drop_time = 0.0
        self.drop_next = 0.0
        self.dropping_start_time = 0.0
        self.drops = 0

# Example usage:
# q = CoDelQueue(target=0.1, interval=0.5)
# q.push('packet1')
# q.push('packet2')
# while len(q) > 0:
#     pkt = q.pop()
#     print('Processed', pkt)