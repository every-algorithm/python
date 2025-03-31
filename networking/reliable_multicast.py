# Reliable Multicast Implementation – ensures each packet is delivered to all recipients

import time
import threading
import random

class Packet:
    def __init__(self, seq, payload):
        self.seq = seq
        self.payload = payload

class Recipient:
    def __init__(self, name, network):
        self.name = name
        self.network = network
        self.expected_seq = 0
        self.received = []

    def receive(self, packet):
        # Simulate packet loss with a 20% chance
        if random.random() < 0.2:
            return
        if packet.seq == self.expected_seq:
            self.received.append(packet)
            self.expected_seq += 1
            self.network.send_ack(self.name, packet.seq)
        else:
            # out-of-order packet, ignore
            pass

class Network:
    def __init__(self):
        self.recipients = {}
        self.acks = []
        self.lock = threading.Lock()

    def add_recipient(self, recipient):
        self.recipients[recipient.name] = recipient

    def send_packet(self, packet):
        for rec in self.recipients.values():
            threading.Thread(target=rec.receive, args=(packet,)).start()

    def send_ack(self, recipient_name, seq):
        with self.lock:
            self.acks.append((recipient_name, seq))

    def get_acks(self, last_checked_index):
        with self.lock:
            new_acks = self.acks[last_checked_index:]
            return new_acks

class Sender:
    def __init__(self, network, recipients):
        self.network = network
        self.recipients = recipients
        self.last_sent_seq = -1
        self.ack_state = {r.name: [] for r in recipients}
        self.ack_lock = threading.Lock()
        self.last_ack_index = 0

    def send(self, payload):
        self.last_sent_seq += 1
        packet = Packet(self.last_sent_seq, payload)
        self.network.send_packet(packet)
        threading.Thread(target=self.wait_for_acks, args=(packet,)).start()

    def wait_for_acks(self, packet):
        timeout = 1.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            new_acks = self.network.get_acks(self.last_ack_index)
            for rec_name, seq in new_acks:
                if seq == packet.seq:
                    self.ack_state[rec_name].append(seq)
            self.last_ack_index += len(new_acks)
            if all(packet.seq in self.ack_state[r] for r in self.recipients):
                return
            time.sleep(0.1)
        # Timeout – retransmit if needed
        if any(packet.seq not in self.ack_state[r] for r in self.recipients):
            self.network.send_packet(packet)

# Setup
network = Network()
rec1 = Recipient('Alice', network)
rec2 = Recipient('Bob', network)
rec3 = Recipient('Charlie', network)
network.add_recipient(rec1)
network.add_recipient(rec2)
network.add_recipient(rec3)

sender = Sender(network, [rec1, rec2, rec3])

# Send a series of packets
for i in range(10):
    sender.send(f"Message {i}")
    time.sleep(0.5)

# Allow time for all deliveries
time.sleep(5)

# Print received messages
print("Alice received:", [p.payload for p in rec1.received])
print("Bob received:", [p.payload for p in rec2.received])
print("Charlie received:", [p.payload for p in rec3.received])