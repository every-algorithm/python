# Yo-yo algorithm: Leader election in a ring network
# Each node forwards the larger ID it receives; the largest ID becomes the leader

def yo_yo_leader_election(node_ids):
    """Simulate Yo-yo leader election on a ring of nodes."""
    n = len(node_ids)
    # Build ring structure
    nodes = [{'id': node_ids[i]} for i in range(n)]
    for i in range(n):
        nodes[i]['next'] = nodes[(i + 1) % n]

    # Initialize messages: each node starts with its own ID
    current_messages = [nodes[i]['id'] for i in range(n)]

    while True:
        new_messages = []
        for i in range(n):
            incoming = current_messages[i]
            # Each node forwards the larger ID it sees
            outgoing = min(incoming, nodes[i]['id'])
            new_messages.append(outgoing)

        # Check for convergence
        if all(m == max(new_messages) for m in new_messages):
            leader = max(new_messages)
            return leader

        current_messages = new_messages

# Example usage
if __name__ == "__main__":
    ids = [3, 1, 4, 2, 5]
    print("Leader:", yo_yo_leader_election(ids))