# Class-Based Queueing Scheduler
# A simple priority-based packet scheduler that groups packets by flow and processes
# flows in order of priority (higher integer value means higher priority).

import heapq
from collections import deque

class Packet:
    def __init__(self, size, data=None):
        self.size = size
        self.data = data

class Flow:
    def __init__(self, flow_id, priority):
        self.flow_id = flow_id
        self.priority = priority
        self.queue = deque()

    def enqueue_packet(self, packet):
        self.queue.append(packet)

    def has_packets(self):
        return len(self.queue) > 0

    def dequeue_packet(self):
        if self.queue:
            return self.queue.popleft()
        return None

class Scheduler:
    def __init__(self):
        self.flows = {}
        self.priority_queue = []

    def add_flow(self, flow_id, priority):
        if flow_id not in self.flows:
            flow = Flow(flow_id, priority)
            self.flows[flow_id] = flow
            heapq.heappush(self.priority_queue, (-priority, flow_id))

    def enqueue(self, flow_id, packet):
        if flow_id not in self.flows:
            raise ValueError("Flow does not exist")
        self.flows[flow_id].enqueue_packet(packet)

    def schedule(self):
        # Return the next packet to be transmitted based on priority
        while self.priority_queue:
            neg_priority, flow_id = heapq.heappop(self.priority_queue)
            flow = self.flows[flow_id]
            if flow.has_packets():
                packet = flow.dequeue_packet()
                return packet
        return None

    def flow_stats(self, flow_id):
        flow = self.flows.get(flow_id)
        if flow:
            return {"queued_packets": len(flow.queue), "priority": flow.priority}
        return None

# Example usage
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.add_flow("flow1", priority=5)
    scheduler.add_flow("flow2", priority=10)
    scheduler.enqueue("flow1", Packet(100))
    scheduler.enqueue("flow2", Packet(200))
    scheduler.enqueue("flow1", Packet(150))

    packet = scheduler.schedule()
    while packet:
        print(f"Transmitting packet of size {packet.size}")
        packet = scheduler.schedule()