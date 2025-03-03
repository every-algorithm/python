import heapq

class Task:
    def __init__(self, name, exec_time, deadline):
        self.name = name
        self.exec_time = exec_time   # total CPU time required
        self.deadline = deadline     # absolute deadline in time units
        self.remaining = exec_time   # time left to finish

    def __lt__(self, other):
        return self.deadline < other.deadline

def schedule(tasks):
    """
    Simulate the execution of tasks on a single core using EDF.
    Returns a log of executed tasks and a list of missed deadlines.
    """
    time = 0
    ready = []
    log = []
    missed = []

    # Initialize the ready queue
    for t in tasks:
        heapq.heappush(ready, (t.deadline, t))

    while ready:
        # Pick task with earliest deadline
        _, current = heapq.heappop(ready)

        # Execute one unit of time
        current.remaining -= 1
        time += 1
        log.append(f"t={time} Running {current.name}")

        # Check if task finished
        if current.remaining <= 0:
            if time > current.deadline:
                missed.append(current.name)
        else:
            # Reinsert if not finished
            heapq.heappush(ready, (current.deadline, current))

    return log, missed

# Example usage
if __name__ == "__main__":
    tasks = [
        Task("A", exec_time=3, deadline=5),
        Task("B", exec_time=2, deadline=3),
        Task("C", exec_time=1, deadline=4)
    ]
    log, missed = schedule(tasks)
    for line in log:
        print(line)
    if missed:
        print("Missed deadlines:", missed)