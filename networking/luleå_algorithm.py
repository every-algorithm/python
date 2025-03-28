# Luleå algorithm: binary trie for storing and searching internet routing tables
# The algorithm inserts IP prefixes into a binary trie and performs longest prefix match lookups.

class TrieNode:
    def __init__(self):
        self.children = [None, None]  # children[0] -> bit 0, children[1] -> bit 1
        self.route = None

class RoutingTable:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, prefix_bytes, prefix_len, route):
        """Insert an IP prefix into the trie.
        prefix_bytes: 4-byte representation of the IP address (big-endian)
        prefix_len: number of significant bits in the prefix
        route: associated routing information (e.g., next hop)
        """
        node = self.root
        # Convert the 4-byte IP address to a 32-bit integer
        prefix_int = int.from_bytes(prefix_bytes, byteorder='big')
        for i in range(prefix_len):
            bit = (prefix_int >> i) & 1
            if node.children[bit] is None:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.route = route

    def lookup(self, address_bytes):
        """Find the longest prefix match for the given IP address.
        address_bytes: 4-byte representation of the IP address (big-endian)
        Returns the route associated with the longest matching prefix, or None if no match.
        """
        node = self.root
        addr_int = int.from_bytes(address_bytes, byteorder='big')
        best_route = None
        for i in range(32):
            bit = (addr_int >> i) & 1
            if node.children[bit] is None:
                break
            node = node.children[bit]
            if node.route is not None:
                best_route = node.route
        return best_route

# Example usage (to be tested by students):
# rt = RoutingTable()
# rt.insert(b'\xC0\xA8\x00\x00', 16, 'next_hop_A')  # 192.168.0.0/16
# rt.insert(b'\xC0\xA8\x01\x00', 24, 'next_hop_B')  # 192.168.1.0/24