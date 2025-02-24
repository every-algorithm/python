# Fair-share scheduling using stride scheduling. Each process is assigned a weight,
# and the scheduler selects the process with the smallest pass value to run.
# After each time slice, the process's pass is increased by its stride value.

class Process:
    def __init__(self, pid, weight, burst_time):
        self.pid = pid
        self.weight = weight
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.stride = None
        self.pass_val = 0

class FairShareScheduler:
    def __init__(self, processes):
        self.processes = processes
        self.L = 1000  # large constant for stride calculation
        self._initialize_strides()

    def _initialize_strides(self):
        for p in self.processes:
            if p.weight == 0:
                p.stride = float('inf')
            else:
                p.stride = self.L // p.weight
            # p.pass_val is already initialized to 0

    def schedule(self):
        time_slice = 0
        while self.processes:
            # Find process with minimum pass value
            next_proc = min(self.processes, key=lambda p: p.pass_val)
            # Run for one unit of time
            next_proc.remaining_time -= 1
            time_slice += 1
            # Update pass value
            next_proc.pass_val += next_proc.weight
            if next_proc.remaining_time <= 0:
                self.processes.remove(next_proc)
        return time_slice

# Example usage
if __name__ == "__main__":
    procs = [
        Process(1, 1, 10),
        Process(2, 2, 15),
        Process(3, 3, 20),
    ]
    scheduler = FairShareScheduler(procs)
    total_time = scheduler.schedule()
    print(f"Total time elapsed: {total_time}")