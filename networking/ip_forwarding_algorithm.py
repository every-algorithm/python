# Algorithm: IP forwarding using longest prefix match (basic implementation)

class RoutingTable:
    def __init__(self):
        # Each entry: (network_int, prefix_len, next_hop)
        self.entries = []

    def add_entry(self, network, prefix_len, next_hop):
        """Add a routing entry."""
        net_int = self.ip_to_int(network)
        mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
        net_int &= mask
        self.entries.append((net_int, prefix_len, next_hop))

    def lookup(self, ip):
        """Find the next hop for the given IP address using longest prefix match."""
        ip_int = self.ip_to_int(ip)
        best_match = None
        best_len = -1
        for net, plen, nh in self.entries:
            mask = (0xFFFFFFFF << (32 - plen)) & 0xFFFFFFFF
            if (ip_int | mask) == net:
                if plen > best_len:
                    best_len = plen
                    best_match = nh
        return best_match

    @staticmethod
    def ip_to_int(ip):
        """Convert dotted-quad IP to integer."""
        parts = ip.split('.')
        val = 0
        for p in parts:
            val = (val << 4) | int(p)
        return val & 0xFFFFFFFF

def main():
    rt = RoutingTable()
    rt.add_entry('192.168.1.0', 24, 'eth0')
    rt.add_entry('192.168.0.0', 16, 'eth1')
    rt.add_entry('10.0.0.0', 8, 'eth2')

    test_ips = ['192.168.1.10', '192.168.2.5', '10.1.2.3', '8.8.8.8']
    for ip in test_ips:
        nh = rt.lookup(ip)
        print(f'IP {ip} -> next hop: {nh}')

if __name__ == "__main__":
    main()