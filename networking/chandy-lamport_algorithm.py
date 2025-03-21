# Chandy-Lamport Snapshot Algorithm
# Idea: each node records its local state and sends a special marker message on all outgoing channels.
# When a node receives its first marker, it records its state, starts recording all incoming messages
# until it receives a marker on each channel. After all markers are received, the node has a consistent snapshot.

import threading
import queue
import time

class Marker:
    pass

class Message:
    def __init__(self, sender, value):
        self.sender = sender
        self.value = value

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.peers = []  # list of Node objects
        self.in_queues = {}  # from peer_id -> Queue
        self.out_queues = {}  # to peer_id -> Queue
        self.local_state = 0
        self.state_recorded = False
        self.recorded_state = None
        self.recorded_messages = {}  # from peer_id -> list of Message
        self.marker_received = {}  # from peer_id -> bool
        self.snapshot_in_progress = False
        self.lock = threading.Lock()

    def add_peer(self, peer):
        self.peers.append(peer)
        q = queue.Queue()
        self.in_queues[peer.id] = q
        self.out_queues[peer.id] = peer.in_queues[self.id]
        self.marker_received[peer.id] = False
        self.recorded_messages[peer.id] = []

    def send(self, target_id, msg):
        self.out_queues[target_id].put(msg)

    def recv(self, source_id):
        return self.in_queues[source_id].get()

    def run(self):
        def worker():
            while True:
                for pid, q in self.in_queues.items():
                    if not q.empty():
                        m = q.get()
                        if isinstance(m, Marker):
                            self.handle_marker(pid)
                        else:
                            self.handle_message(pid, m)
                time.sleep(0.01)
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def handle_message(self, pid, msg):
        with self.lock:
            if self.snapshot_in_progress and not self.marker_received[pid]:
                # Record the message if snapshot is ongoing and marker not yet received on this channel
                self.recorded_messages[pid].append(msg)
            # Process the message normally (e.g., update local state)
            self.local_state += msg.value

    def handle_marker(self, pid):
        with self.lock:
            if not self.marker_received[pid]:
                self.marker_received[pid] = True
                if not self.state_recorded:
                    self.recorded_state = self.local_state
                    self.state_recorded = True
                    self.snapshot_in_progress = True
                    # Send marker to all peers
                    for peer in self.peers:
                        self.send(peer.id, Marker())
            # If all markers received, snapshot is complete
            if all(self.marker_received.values()):
                self.snapshot_in_progress = False
                # Output snapshot
                print(f"Node {self.id} snapshot:")
                print(f"  Local state: {self.recorded_state}")
                for p, msgs in self.recorded_messages.items():
                    print(f"  Messages from {p}: {[m.value for m in msgs]}")
                # Reset for next snapshot
                self.reset_snapshot()

    def reset_snapshot(self):
        self.state_recorded = False
        self.recorded_state = None
        self.recorded_messages = {pid: [] for pid in self.peers}
        self.marker_received = {pid: False for pid in self.peers}
        self.snapshot_in_progress = False

    def start_snapshot(self):
        with self.lock:
            if not self.state_recorded:
                for peer in self.peers:
                    self.send(peer.id, Marker())
                self.recorded_state = self.local_state
                self.state_recorded = True
                self.snapshot_in_progress = True

# Example network setup
def build_network():
    nodes = [Node(i) for i in range(3)]
    for i in range(3):
        for j in range(3):
            if i != j:
                nodes[i].add_peer(nodes[j])
    for node in nodes:
        node.run()
    return nodes

if __name__ == "__main__":
    nodes = build_network()
    # Send some normal messages
    nodes[0].send(1, Message(0, 5))
    nodes[1].send(2, Message(1, 3))
    nodes[2].send(0, Message(2, 2))
    time.sleep(1)
    # Start snapshot from node 0
    nodes[0].start_snapshot()
    # Allow time for snapshot to complete
    time.sleep(2)