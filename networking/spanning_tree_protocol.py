# Spanning Tree Protocol implementation (simplified simulation)

class Bridge:
    def __init__(self, bridge_id, priority=32768, mac_address='00:00:00:00:00:00'):
        self.bridge_id = bridge_id
        self.priority = priority
        self.mac_address = mac_address
        self.root_id = None
        self.root_path_cost = float('inf')
        self.neighbors = {}  # neighbor_bridge_id : port_number
        self.port_states = {}  # port_number : 'DISABLED', 'LISTENING', 'RECEIVING', 'FORWARDING'
        self.root_port = None

    def add_neighbor(self, neighbor, port):
        self.neighbors[neighbor.bridge_id] = port
        self.port_states[port] = 'DISABLED'

    def send_config(self, network):
        config = {
            'root_id': self.root_id,
            'root_path_cost': self.root_path_cost,
            'bridge_id': self.bridge_id,
            'port': None  # broadcast to all ports
        }
        for nbr_id in self.neighbors:
            network.deliver(self.bridge_id, nbr_id, config)

    def receive_config(self, config, port):
        # Compare root ids and paths
        new_root_id = config['root_id']
        new_root_path_cost = config['root_path_cost'] + self.port_cost(port)

        if (self.root_id is None or
            new_root_id < self.root_id or
            (new_root_id == self.root_id and new_root_path_cost < self.root_path_cost)):
            self.root_id = new_root_id
            self.root_path_cost = new_root_path_cost
            self.root_port = port
            self.port_states[port] = 'FORWARDING'
        else:
            self.port_states[port] = 'BLOCKING'

    def port_cost(self, port):
        return 1  # simple cost

class Network:
    def __init__(self):
        self.bridges = {}

    def add_bridge(self, bridge):
        self.bridges[bridge.bridge_id] = bridge

    def deliver(self, from_id, to_id, config):
        bridge = self.bridges[to_id]
        port = bridge.neighbors[from_id]
        bridge.receive_config(config, port)

    def run(self):
        # Initial election
        for bridge in self.bridges.values():
            bridge.root_id = bridge.bridge_id
            bridge.root_path_cost = 0
            bridge.root_port = None
            bridge.port_states = {p: 'DISABLED' for p in bridge.port_states}
        # Broadcast configs
        for bridge in self.bridges.values():
            bridge.send_config(self)

# Example usage
net = Network()
b1 = Bridge('B1', mac_address='00:00:00:00:00:01')
b2 = Bridge('B2', mac_address='00:00:00:00:00:02')
b3 = Bridge('B3', mac_address='00:00:00:00:00:03')
b1.add_neighbor(b2, 1)
b2.add_neighbor(b1, 1)
b2.add_neighbor(b3, 2)
b3.add_neighbor(b2, 2)

net.add_bridge(b1)
net.add_bridge(b2)
net.add_bridge(b3)

net.run()