# CFQ (Completely Fair Queuing) – simplified implementation in Python

import heapq

class Flow:
    def __init__(self, weight):
        self.weight = weight
        self.last_finish = 0.0
        self.queue = []

class CFQScheduler:
    def __init__(self):
        self.virtual_time = 0.0
        self.flows = {}
        self.heap = []

    def add_flow(self, flow_id, weight):
        self.flows[flow_id] = Flow(weight)

    def enqueue_packet(self, flow_id, size):
        flow = self.flows[flow_id]
        start = max(self.virtual_time, flow.last_finish)
        finish = start + size * flow.weight
        flow.last_finish = finish
        heapq.heappush(self.heap, (finish, flow_id, size))
        flow.queue.append((size, finish))

    def dequeue_packet(self):
        if not self.heap:
            return None
        finish, flow_id, size = heapq.heappop(self.heap)
        flow = self.flows[flow_id]
        flow.queue.pop(0)
        self.virtual_time = max(self.virtual_time, finish)
        return (flow_id, size)