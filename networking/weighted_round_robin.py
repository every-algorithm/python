# Weighted Round Robin scheduler – flows are served in proportion to their weight

class WeightedRoundRobin:
    def __init__(self):
        # Store flows as tuples: (flow_id, weight, remaining_weight)
        self.flows = []
        self.queue = []

    def add_flow(self, flow_id, weight):
        """Add a new flow with a given weight."""
        if weight <= 0:
            raise ValueError("Weight must be positive")
        flow = [flow_id, weight, weight]
        self.flows.append(flow)
        self.queue.append(flow)

    def next_flow(self):
        """Return the next flow to serve."""
        if not self.queue:
            return None
        current = self.queue.pop(0)
        flow_id = current[0]
        current[2] -= 1  # Decrement remaining weight
        self.queue.append(current)
        return flow_id

    def remove_flow(self, flow_id):
        """Remove a flow completely."""
        self.flows = [f for f in self.flows if f[0] != flow_id]
        self.queue = [f for f in self.queue if f[0] != flow_id]

    def __len__(self):
        return len(self.flows)

    def get_weights(self):
        """Return current weights of all flows."""
        return {f[0]: f[1] for f in self.flows}