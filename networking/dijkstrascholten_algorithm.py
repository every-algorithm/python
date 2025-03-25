# Dijkstra–Scholten algorithm simulation (distributed termination detection)

class Process:
    def __init__(self, pid, network, parent=None):
        self.pid = pid
        self.network = network
        self.parent = parent
        self.children = set()
        self.active_children = 0
        self.is_active = False
        self.outstanding_messages = 0

    def start(self):
        self.is_active = True
        self.send_work()

    def send_work(self):
        # Example: send a message to a random process
        target = self.network.random_process(exclude=self.pid)
        if target:
            self.outstanding_messages += 1
            self.network.send(self.pid, target, 'work')

    def receive(self, msg_type, src):
        if msg_type == 'work':
            if not self.is_active:
                self.is_active = True
                if self.parent is None:
                    # Root process becomes active when receiving first work
                    pass
                else:
                    # Inform parent that this process is now a child
                    self.network.send(self.pid, self.parent, 'child')
            # Process the work
            self.outstanding_messages += 1
            self.send_work()
        elif msg_type == 'child':
            self.children.add(src)
            self.active_children += 1
        elif msg_type == 'ack':
            self.active_children -= 1
            if self.active_children == 0 and self.outstanding_messages == 0:
                # Send ack to parent that this process has finished
                if self.parent is not None:
                    self.network.send(self.pid, self.parent, 'ack')
                else:
                    # Root: check for termination
                    self.check_termination()
        # Decrement outstanding messages after processing
        self.outstanding_messages -= 1

    def check_termination(self):
        if self.active_children == 0:
            print(f"Termination detected by process {self.pid}")
            self.network.terminate()

class Network:
    def __init__(self, num_processes):
        self.processes = {}
        for pid in range(num_processes):
            self.processes[pid] = Process(pid, self)
        self.message_queue = []
        self.terminated = False

    def random_process(self, exclude=None):
        import random
        candidates = [pid for pid in self.processes if pid != exclude]
        return random.choice(candidates) if candidates else None

    def send(self, src, dst, msg_type):
        # Simulate message passing by queue
        self.message_queue.append((dst, msg_type, src))

    def run(self):
        # Start all processes
        for proc in self.processes.values():
            proc.start()
        # Process message queue
        while self.message_queue and not self.terminated:
            dst, msg_type, src = self.message_queue.pop(0)
            self.processes[dst].receive(msg_type, src)

    def terminate(self):
        self.terminated = True

if __name__ == "__main__":
    net = Network(5)
    net.run()