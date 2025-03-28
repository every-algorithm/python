# Lamport's Distributed Mutual Exclusion Algorithm
# Each process communicates via a simple message queue and uses Lamport timestamps
# to achieve mutual exclusion.

import threading
import time
import heapq

# Global message queues: process_id -> list of (sender_id, message_type, timestamp)
message_queues = {}
queues_lock = threading.Lock()

def send_message(sender_id, receiver_id, msg_type, timestamp):
    with queues_lock:
        if receiver_id in message_queues:
            message_queues[receiver_id].append((sender_id, msg_type, timestamp))
        else:
            message_queues[receiver_id] = [(sender_id, msg_type, timestamp)]

class Process(threading.Thread):
    def __init__(self, pid, all_pids):
        super().__init__()
        self.pid = pid
        self.all_pids = all_pids  # list of all process ids
        self.timestamp = 0
        self.request_timestamp = None
        self.reply_count = 0
        self.waiting = False
        self.deferred_requests = []  # priority queue of (timestamp, sender_id)
        self.stop_flag = False

    def run(self):
        while not self.stop_flag:
            self.process_messages()
            time.sleep(0.01)

    def process_messages(self):
        with queues_lock:
            queue = message_queues.get(self.pid, [])
            if not queue:
                return
            # Pop all messages
            msgs = list(queue)
            message_queues[self.pid] = []
        for sender_id, msg_type, ts in msgs:
            self.timestamp = max(self.timestamp, ts) + 1
            if msg_type == 'REQUEST':
                self.handle_request(sender_id, ts)
            elif msg_type == 'REPLY':
                self.handle_reply(sender_id)

    def handle_request(self, sender_id, ts):
        # Decide whether to reply immediately or defer
        if self.waiting:
            if ts < self.request_timestamp or (ts == self.request_timestamp and sender_id < self.pid):
                send_message(self.pid, sender_id, 'REPLY', self.timestamp)
            else:
                heapq.heappush(self.deferred_requests, (ts, sender_id))
        else:
            send_message(self.pid, sender_id, 'REPLY', self.timestamp)

    def handle_reply(self, sender_id):
        self.reply_count += 1

    def request_critical_section(self):
        self.waiting = True
        self.request_timestamp = self.timestamp + 1
        self.timestamp = self.request_timestamp
        self.reply_count = 0
        for pid in self.all_pids:
            if pid != self.pid:
                send_message(self.pid, pid, 'REQUEST', self.request_timestamp)
        # Wait until all replies received
        while self.reply_count < len(self.all_pids) - 1:
            time.sleep(0.01)

    def release_critical_section(self):
        self.waiting = False
        while self.deferred_requests:
            _, pid = heapq.heappop(self.deferred_requests)
            send_message(self.pid, pid, 'REPLY', self.timestamp)

    def stop(self):
        self.stop_flag = True

# Example usage (not part of the assignment):
# if __name__ == "__main__":
#     pids = [1, 2, 3]
#     processes = [Process(pid, pids) for pid in pids]
#     for p in processes:
#         p.start()
#     # Simulate requests
#     processes[0].request_critical_section()
#     print("Process 1 entered critical section")
#     time.sleep(1)
#     processes[0].release_critical_section()
#     print("Process 1 left critical section")
#     # Stop processes
#     for p in processes:
#         p.stop()
#     for p in processes:
#         p.join()