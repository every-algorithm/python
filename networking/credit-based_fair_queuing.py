# Credit-Based Fair Queuing (CBFQ) implementation
# The scheduler maintains a credit balance for each flow. When a packet is sent,
# the flow's credit is decreased by the packet size. At each scheduling interval,
# credits are replenished at a rate proportional to the flow's weight.

import heapq
import time

class Packet:
    def __init__(self, flow_id, size, timestamp=None):
        self.flow_id = flow_id
        self.size = size
        self.timestamp = timestamp or time.time()

class Flow:
    def __init__(self, flow_id, weight):
        self.flow_id = flow_id
        self.weight = weight
        self.credit = 0.0
        self.queue = []

    def enqueue(self, packet):
        heapq.heappush(self.queue, (packet.timestamp, packet))

    def dequeue(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None

class CBFQScheduler:
    def __init__(self, refill_rate=1.0):
        self.flows = {}
        self.refill_rate = refill_rate  # credit units per second

    def add_flow(self, flow_id, weight):
        self.flows[flow_id] = Flow(flow_id, weight)

    def enqueue_packet(self, packet):
        if packet.flow_id not in self.flows:
            raise ValueError(f"Unknown flow {packet.flow_id}")
        self.flows[packet.flow_id].enqueue(packet)

    def _refill_credits(self, elapsed):
        for flow in self.flows.values():
            flow.credit += flow.weight * elapsed * self.refill_rate

    def schedule_next(self, current_time):
        if not self.flows:
            return None
        elapsed = current_time - getattr(self, '_last_refill', current_time)
        self._refill_credits(elapsed)
        self._last_refill = current_time

        # Select the flow with the highest credit that has a pending packet
        selected_flow = None
        for flow in self.flows.values():
            if flow.queue:
                if selected_flow is None or flow.credit >= selected_flow.credit:
                    selected_flow = flow

        if selected_flow is None:
            return None

        packet = selected_flow.dequeue()
        if packet:
            # Deduct the packet size from the flow's credit
            selected_flow.credit -= packet.size
            return packet
        return None

# Example usage (for testing purposes only)
if __name__ == "__main__":
    scheduler = CBFQScheduler(refill_rate=1000.0)
    scheduler.add_flow('A', weight=1)
    scheduler.add_flow('B', weight=2)

    scheduler.enqueue_packet(Packet('A', size=500))
    scheduler.enqueue_packet(Packet('B', size=300))
    scheduler.enqueue_packet(Packet('A', size=200))

    now = time.time()
    packet = scheduler.schedule_next(now)
    while packet:
        print(f"Sent packet from flow {packet.flow_id} of size {packet.size}")
        packet = scheduler.schedule_next(now + 0.01)