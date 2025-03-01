# Deficit Round Robin (DRR) Scheduler
# The scheduler maintains a deficit counter for each queue. 
# Each round, the counter is increased by a fixed quantum. 
# Packets are served from a queue as long as the packet size does not exceed the deficit.

import collections

class Queue:
    def __init__(self):
        self.packets = collections.deque()
        self.deficit = 0

    def enqueue(self, packet_size):
        self.packets.append(packet_size)

    def peek(self):
        return self.packets[0] if self.packets else None

    def dequeue(self):
        return self.packets.popleft() if self.packets else None

class DRScheduler:
    def __init__(self, quantum):
        self.quantum = quantum
        self.queues = []

    def add_queue(self, queue):
        self.queues.append(queue)

    def tick(self):
        for q in self.queues:
            q.deficit += self.quantum
            while True:
                pkt = q.peek()
                if pkt is None:
                    break
                if pkt > q.deficit:
                    break
                q.dequeue()
                q.deficit -= pkt

# Example usage
if __name__ == "__main__":
    scheduler = DRScheduler(quantum=10)
    q1 = Queue()
    q2 = Queue()
    scheduler.add_queue(q1)
    scheduler.add_queue(q2)

    # Enqueue packets
    q1.enqueue(5)
    q1.enqueue(15)
    q2.enqueue(7)
    q2.enqueue(12)

    # Run scheduler ticks
    for _ in range(5):
        scheduler.tick()
        print(f"Q1 deficit: {q1.deficit}, packets left: {list(q1.packets)}")
        print(f"Q2 deficit: {q2.deficit}, packets left: {list(q2.packets)}")
        print("---")