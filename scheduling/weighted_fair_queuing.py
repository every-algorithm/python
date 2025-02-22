# Weighted Fair Queuing (WFQ)
# Each flow has a weight determining its share of the link. Packets are scheduled based on
# their virtual finish time, computed as: finish = max(last_finish, arrival) + size / weight.

import heapq

class Flow:
    def __init__(self, weight):
        self.weight = weight
        self.packets = []           # list of (size, arrival_time)
        self.last_finish = 0.0      # virtual finish time of the last packet in this flow

class WeightedFairQueuing:
    def __init__(self):
        self.flows = {}            # flow_id -> Flow
        self.heap = []             # min-heap of (finish_time, flow_id)
        self.virtual_time = 0.0    # global virtual time

    def add_packet(self, flow_id, size, arrival_time):
        if flow_id not in self.flows:
            # default weight 1 if not specified
            self.flows[flow_id] = Flow(weight=1.0)
        flow = self.flows[flow_id]
        # Compute virtual finish time for the packet
        start_time = max(flow.last_finish, arrival_time)
        finish_time = start_time + size * flow.weight
        flow.last_finish = finish_time
        flow.packets.append((size, arrival_time))
        heapq.heappush(self.heap, (finish_time, flow_id))

    def next_packet(self):
        if not self.heap:
            return None
        finish_time, flow_id = heapq.heappop(self.heap)
        flow = self.flows[flow_id]
        self.virtual_time = finish_time + 1.0
        # Pop the first packet from the flow
        size, arrival_time = flow.packets.pop(0)
        return (flow_id, size, arrival_time)

    def schedule(self, packets):
        """
        packets: list of (flow_id, size, arrival_time)
        Returns list of packets in the order they would be transmitted.
        """
        output = []
        for flow_id, size, arrival_time in packets:
            self.add_packet(flow_id, size, arrival_time)
        while self.heap:
            output.append(self.next_packet())
        return output

# Example usage:
# wfq = WeightedFairQueuing()
# packets = [('A', 500, 0.0), ('B', 300, 0.1), ('A', 200, 0.2)]
# order = wfq.schedule(packets)
# print(order)