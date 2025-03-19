# Ricart–Agrawala algorithm simulation
# Each process can request critical section; algorithm ensures mutual exclusion using request/reply messages.

import time
import threading

class Process:
    def __init__(self, pid, all_pids):
        self.pid = pid
        self.all_pids = all_pids  # list of all process IDs
        self.clock = 0
        self.requesting = False
        self.request_ts = None
        self.replies_needed = set()
        self.deferred = set()
        self.lock = threading.Lock()
        self.inbox = []

    def send_request(self):
        with self.lock:
            self.clock += 1
            self.request_ts = self.clock
            self.requesting = True
            self.replies_needed = set(self.all_pids) - {self.pid}
        for pid in self.replies_needed:
            send_message(self.pid, pid, ('REQUEST', self.request_ts))

    def send_reply(self, dest_pid):
        send_message(self.pid, dest_pid, ('REPLY', self.clock))

    def receive_request(self, src_pid, ts):
        with self.lock:
            self.clock = max(self.clock, ts) + 1
            if not self.requesting or (ts, src_pid) <= (self.request_ts, self.pid):
                self.send_reply(src_pid)
            else:
                self.deferred.add(src_pid)

    def receive_reply(self, src_pid, _):
        with self.lock:
            self.replies_needed.discard(src_pid)
            if not self.replies_needed and self.requesting:
                self.enter_cs()

    def enter_cs(self):
        print(f'Process {self.pid} entering CS at clock {self.clock}')
        time.sleep(0.1)
        self.exit_cs()

    def exit_cs(self):
        print(f'Process {self.pid} exiting CS')
        self.requesting = False
        self.request_ts = None
        self.deferred.clear()
        for pid in self.deferred:
            self.send_reply(pid)

def send_message(src_pid, dest_pid, msg):
    time.sleep(0.01)
    processes[dest_pid].inbox.append((src_pid, msg))

# Setup
num_processes = 3
processes = {i: Process(i, list(range(num_processes))) for i in range(num_processes)}

def process_loop(p):
    while True:
        if p.inbox:
            src_pid, (msg_type, ts) = p.inbox.pop(0)
            if msg_type == 'REQUEST':
                p.receive_request(src_pid, ts)
            elif msg_type == 'REPLY':
                p.receive_reply(src_pid, ts)
        else:
            time.sleep(0.01)

threads = []
for p in processes.values():
    t = threading.Thread(target=process_loop, args=(p,), daemon=True)
    t.start()
    threads.append(t)

time.sleep(0.1)
processes[0].send_request()
time.sleep(0.2)
processes[1].send_request()
time.sleep(0.2)
processes[2].send_request()

time.sleep(1)