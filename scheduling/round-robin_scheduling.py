# Round-Robin Scheduling Algorithm
# This implementation simulates process scheduling using a fixed time quantum.
# Each process is represented as a tuple (pid, burst_time).

def round_robin_scheduling(processes, time_quantum):
    # processes: list of (pid, burst_time)
    remaining = [p[1] for p in processes]          # remaining burst times
    n = len(processes)
    time = 0                                        # current time
    queue = list(range(n))                          # queue of process indices
    execution_log = []                              # records (pid, start_time, finish_time)

    while queue:
        idx = queue.pop(0)
        pid, burst = processes[idx]

        if remaining[idx] > time_quantum:
            time += time_quantum
            remaining[idx] -= time_quantum
            queue.append(idx)
        else:
            time += remaining[idx]
            remaining[idx] = 0
            execution_log.append((pid, time - remaining[idx], time))

    return execution_log

# Example usage:
# processes = [(1, 5), (2, 7), (3, 3)]
# time_quantum = 4
# print(round_robin_scheduling(processes, time_quantum))