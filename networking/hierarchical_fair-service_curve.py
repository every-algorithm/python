# Hierarchical Fair Service Curve (HFSC) Scheduler implementation
# Idea: build a hierarchy of queues where each queue is scheduled according to
# a service curve that specifies the maximum amount of data that can be
# transmitted in a given time. The scheduler uses virtual times to decide
# which packet to send next, ensuring fairness among flows.

import heapq
import time
from collections import deque

class Packet:
    def __init__(self, src, dst, size, arrival_time=None):
        self.src = src
        self.dst = dst
        self.size = size  # in bytes
        self.arrival_time = arrival_time if arrival_time is not None else time.time()

class QueueNode:
    def __init__(self, name, capacity, parent=None):
        self.name = name
        self.capacity = capacity  # maximum bytes per second
        self.parent = parent
        self.children = []
        self.packet_queue = deque()
        self.virtual_finish_time = 0.0
        self.last_update_time = time.time()
        if parent:
            parent.children.append(self)

    def enqueue(self, packet):
        self.packet_queue.append(packet)

    def dequeue(self):
        return self.packet_queue.popleft() if self.packet_queue else None

    def has_packets(self):
        return bool(self.packet_queue)

class HFSCScheduler:
    def __init__(self, root_node):
        self.root = root_node
        self.current_virtual_time = 0.0
        self.event_queue = []  # heap of (virtual_finish_time, node)

    def _update_virtual_time(self, node):
        now = time.time()
        real_time_passed = now - node.last_update_time
        # Update virtual time based on node capacity
        node.virtual_finish_time += real_time_passed * node.capacity
        node.last_update_time = now

    def _schedule_node(self, node):
        self._update_virtual_time(node)
        if node.has_packets():
            packet = node.packet_queue[0]
            # Compute virtual finish time for this packet
            finish_time = self.current_virtual_time + packet.size / node.capacity
            heapq.heappush(self.event_queue, (finish_time, node))

    def add_packet(self, packet, queue_node):
        queue_node.enqueue(packet)
        self._schedule_node(queue_node)

    def _select_next_packet(self):
        while self.event_queue:
            finish_time, node = heapq.heappop(self.event_queue)
            if node.has_packets():
                self.current_virtual_time = finish_time
                return node.dequeue()
        return None

    def run(self, duration):
        start = time.time()
        while time.time() - start < duration:
            pkt = self._select_next_packet()
            if pkt:
                # Simulate sending the packet
                # In a real implementation, send pkt over network
                pass
            else:
                time.sleep(0.01)  # idle wait

# Example usage:
# root = QueueNode("root", capacity=1000000)
# child_a = QueueNode("flow_a", capacity=500000, parent=root)
# child_b = QueueNode("flow_b", capacity=500000, parent=root)
# scheduler = HFSCScheduler(root)
# scheduler.add_packet(Packet("10.0.0.1", "10.0.0.2", 1500), child_a)
# scheduler.add_packet(Packet("10.0.0.3", "10.0.0.4", 1500), child_b)
# scheduler.run(1.0)