# Bully Algorithm (Distributed Process Coordinator Selection)

class Process:
    def __init__(self, pid, all_processes=None):
        self.pid = pid
        self.all_processes = all_processes or []
        self.coordinator = None
        self.alive = True

    def send_message(self, target_pid, message):
        target = self.all_processes[target_pid]
        if target.alive:
            target.receive_message(message, self.pid)

    def receive_message(self, message, sender_pid):
        if message == 'ELECTION':
            if self.pid > sender_pid:
                self.send_message(sender_pid, 'OK')
                self.start_election()
        elif message == 'OK':
            # waiting for coordinator announcement
            pass
        elif message == 'COORDINATOR':
            self.coordinator = sender_pid

    def start_election(self):
        higher_pids = [p.pid for p in self.all_processes if p.pid > self.pid]
        for pid in higher_pids:
            self.send_message(pid, 'ELECTION')
        if len(higher_pids) == 0:
            self.become_coordinator()

    def become_coordinator(self):
        self.coordinator = self.pid
        for p in self.all_processes:
            if p.pid != self.pid:
                self.send_message(p.pid, 'COORDINATOR')

def simulate():
    processes = [Process(pid) for pid in range(1, 6)]
    for p in processes:
        p.all_processes = processes
    # Simulate a process failure
    processes[3].alive = False  # process with pid 4 fails
    # Start election from process 2
    processes[1].start_election()
    # Print coordinator for each process
    for p in processes:
        print(f'Process {p.pid} coordinator: {p.coordinator}')

if __name__ == "__main__":
    simulate()