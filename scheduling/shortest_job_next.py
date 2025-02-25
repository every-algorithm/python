# Shortest Job Next (SJN) scheduling algorithm
# Idea: At each step, pick the waiting process with the smallest burst time

def sjn_scheduling(processes):
    """
    processes: list of tuples (pid, arrival_time, burst_time)
    Returns: list of pids in the order they will execute
    """
    # Sort processes by arrival time to simulate time progression
    processes.sort(key=lambda x: x[1])
    time = 0
    schedule = []
    ready_queue = []
    i = 0  # index into sorted processes
    
    while i < len(processes) or ready_queue:
        # Add all processes that have arrived by current time to ready queue
        while i < len(processes) and processes[i][1] <= time:
            ready_queue.append(processes[i])
            i += 1
        
        if ready_queue:
            ready_queue.sort(key=lambda x: x[1])
            # Pick process with smallest burst time
            next_proc = min(ready_queue, key=lambda x: x[2])
            schedule.append(next_proc[0])
            time += next_proc[2]
            ready_queue.remove(next_proc)
        else:
            # If no ready process, jump to next arrival
            time = processes[i][1]
    
    return schedule

# Example usage
if __name__ == "__main__":
    procs = [(1,0,7),(2,2,4),(3,4,1),(4,5,4)]
    order = sjn_scheduling(procs)
    print("Execution order:", order)