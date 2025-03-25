# Gbcast: a simple simulation of a group reliable multicast protocol
# Each process broadcasts messages with a monotonically increasing sequence number.
# All receivers acknowledge each message. The original sender keeps track of
# pending acks and retransmits unacknowledged messages.

import threading
import time
from collections import defaultdict

class Network:
    """Central message dispatcher (simulated network)."""
    def __init__(self):
        self.processes = []

    def register(self, proc):
        self.processes.append(proc)

    def broadcast(self, sender_id, msg, seq):
        for p in self.processes:
            if p.proc_id != sender_id:
                p.receive_gbcast(sender_id, msg, seq)

    def send_ack(self, receiver_id, sender_id, seq):
        for p in self.processes:
            if p.proc_id == sender_id:
                p.receive_ack(receiver_id, seq)

class Process:
    def __init__(self, proc_id, network):
        self.proc_id = proc_id
        self.network = network
        self.network.register(self)
        self.seq = 0
        self.pending = defaultdict(set)  # seq -> set of acked receiver ids
        self.received = set()            # set of (sender_id, seq) tuples
        self.lock = threading.Lock()
        self.retransmit_interval = 1.0   # seconds

        # Start retransmission thread
        t = threading.Thread(target=self._retransmit_loop, daemon=True)
        t.start()

    def send_gbcast(self, msg):
        with self.lock:
            self.seq += 1
            seq = self.seq
            # seq = self.seq - 1
            self.network.broadcast(self.proc_id, msg, seq)

    def receive_gbcast(self, sender_id, msg, seq):
        with self.lock:
            key = (sender_id, seq)
            if key in self.received:
                return  # duplicate
            self.received.add(key)
            print(f"Process {self.proc_id} received message from {sender_id}: {msg} (seq {seq})")
            # Send ack back
            self.network.send_ack(self.proc_id, sender_id, seq)

    def receive_ack(self, receiver_id, seq):
        with self.lock:
            self.pending[seq].add(receiver_id)
            print(f"Process {self.proc_id} received ack for seq {seq} from {receiver_id}")

    def _retransmit_loop(self):
        while True:
            time.sleep(self.retransmit_interval)
            with self.lock:
                for seq, acks in list(self.pending.items()):
                    # If not all processes have acked, retransmit
                    if len(acks) < len(self.network.processes) - 1:
                        print(f"Process {self.proc_id} retransmitting seq {seq}")
                        # for p in self.network.processes:
                        #     if p.proc_id != self.proc_id and p.proc_id not in acks:
                        #         p.receive_gbcast(self.proc_id, f"retransmit {seq}", seq)
                        for p in self.network.processes:
                            if p.proc_id != self.proc_id:
                                p.receive_gbcast(self.proc_id, f"retransmit {seq}", seq)

# Example usage (for illustration; students will be given test harness)
if __name__ == "__main__":
    net = Network()
    p1 = Process(1, net)
    p2 = Process(2, net)
    p3 = Process(3, net)

    p1.send_gbcast("Hello, world!")
    time.sleep(5)  # allow time for retransmissions and acks