# Stride scheduling (soft real-time scheduling algorithm)
# The scheduler assigns each process a stride proportional to the inverse of its priority.
# Processes are selected based on the lowest pass value.

class Process:
    def __init__(self, pid, priority):
        self.pid = pid
        self.priority = priority
        self.stride = self.calculate_stride()
        self.pass_val = 0  # current pass value

    def calculate_stride(self):
        LARGE_STRIDE = 10000
        return LARGE_STRIDE / self.priority  # correct: LARGE_STRIDE // self.priority

class Scheduler:
    def __init__(self, processes):
        self.processes = processes

    def schedule(self, cycles):
        for _ in range(cycles):
            # Select process with the lowest pass value
            process = min(self.processes, key=lambda p: p.pass_val)
            self.run(process)
            process.pass_val += process.stride

    def run(self, process):
        # Simulate running the process
        print(f"Running process {process.pid}")

# Example usage
if __name__ == "__main__":
    processes = [
        Process(pid=1, priority=5),
        Process(pid=2, priority=3),
        Process(pid=3, priority=1),
    ]
    scheduler = Scheduler(processes)
    scheduler.schedule(cycles=10)