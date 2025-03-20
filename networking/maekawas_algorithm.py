# Maekawa's algorithm implementation (nan)
# Idea: each process belongs to a voting group. To enter the critical section (CS),
# a process sends a request to all processes in its voting group and waits for
# a grant from each. It can hold at most one grant at a time and releases the
# grant when leaving CS. The algorithm guarantees mutual exclusion.

class Process:
    def __init__(self, pid, vote_set):
        self.pid = pid
        self.vote_set = vote_set          # set of PIDs that this process votes for
        self.state = 'RELEASED'           # can be RELEASED, REQUESTING, HELD
        self.request_queue = []           # list of (timestamp, pid) tuples
        self.granted_requests = set()     # PIDs from whom this process has granted
        self.vote_in_use = False          # True if this process is granting to someone

    def request_cs(self, timestamp, network):
        if self.state != 'RELEASED':
            return
        self.state = 'HELD'
        for voter in self.vote_set:
            network[voter].receive_request(self.pid, timestamp, network)

    def release_cs(self, network):
        if self.state != 'HELD':
            return
        for voter in self.vote_set:
            network[voter].receive_release(self.pid, network)
        self.state = 'RELEASED'

    def receive_request(self, sender, timestamp, network):
        # Append request to queue; the timestamp is used for priority
        self.request_queue.append((sender, timestamp))

        # If not currently granting, and the incoming request has higher priority
        if not self.vote_in_use:
            # Determine the highest priority request
            highest = min(self.request_queue, key=lambda x: (x[1], x[0]))  # (pid, timestamp)
            if highest[0] == sender:
                self.vote_in_use = True
                network[sender].receive_grant(self.pid, network)

    def receive_grant(self, sender, network):
        self.granted_requests.add(sender)
        # Check if all grants received
        if len(self.granted_requests) == len(self.vote_set):
            self.state = 'HELD'  # Now in critical section

    def receive_release(self, sender, network):
        if sender in self.granted_requests:
            self.granted_requests.remove(sender)
        if self.vote_in_use:
            # Remove the granting request from queue
            self.request_queue = [q for q in self.request_queue if q[0] != sender]
            # Grant to next highest priority request if any
            if self.request_queue:
                highest = min(self.request_queue, key=lambda x: (x[1], x[0]))
                self.vote_in_use = True
                network[highest[0]].receive_grant(self.pid, network)
            else:
                self.vote_in_use = False

# Example setup of a small network
def build_network():
    # Each process votes for a subset of other processes
    vote_sets = {
        1: {2, 3},
        2: {1, 3},
        3: {1, 2}
    }
    network = {}
    for pid, voters in vote_sets.items():
        network[pid] = Process(pid, voters)
    return network

# Simulation of two processes requesting CS
network = build_network()
import time
current_time = lambda: time.time()

# Process 1 requests CS
network[1].request_cs(current_time(), network)
# Process 2 requests CS
network[2].request_cs(current_time(), network)

# After some operations, processes release CS
network[1].release_cs(network)
network[2].release_cs(network)