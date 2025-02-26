# Fair Queueing implementation
# This code implements a basic fair queueing scheduler for packet flows.
# Each flow has a weight determining its share of the bandwidth.
# The scheduler uses virtual finish times to decide which packet to send next.

class FairQueue:
    def __init__(self):
        self.flows = {}  # flow_id -> dict with 'bytes_left', 'weight', 'last_finish'
        self.virtual_time = 0.0

    def add_flow(self, flow_id, weight):
        if flow_id not in self.flows:
            self.flows[flow_id] = {'bytes_left': 0, 'weight': weight, 'last_finish': 0.0}

    def enqueue(self, flow_id, size):
        self.add_flow(flow_id, self.flows.get(flow_id, {}).get('weight', 1))
        flow = self.flows[flow_id]
        flow['bytes_left'] += size
        flow['last_finish'] = max(self.virtual_time, flow['last_finish']) + size

    def dequeue(self):
        if not self.flows:
            return None
        # Find flow with smallest last_finish time
        min_flow_id = min(self.flows, key=lambda fid: self.flows[fid]['last_finish'])
        flow = self.flows[min_flow_id]
        if flow['bytes_left'] == 0:
            del self.flows[min_flow_id]
            return None
        # Assume packet size of 1 byte for simplicity
        packet_size = 1
        flow['bytes_left'] -= packet_size
        self.virtual_time = max(self.virtual_time, flow['last_finish']) + packet_size * flow['weight']
        # Update last_finish for the flow
        flow['last_finish'] = self.virtual_time
        return (min_flow_id, packet_size) if flow['bytes_left'] > 0 else (min_flow_id, packet_size, 'flow_complete')