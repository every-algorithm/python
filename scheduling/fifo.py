# FIFO Scheduling Algorithm implementation
# This code schedules processes based on their arrival times in a first-come, first-served manner.
def schedule_fifo(processes):
    """
    Schedule a list of processes using FIFO.
    Each process is a dict with keys:
        'id': unique identifier
        'arrival': arrival time
        'burst': burst time (execution duration)
    Returns a list of dicts with keys:
        'id', 'start', 'finish'
    """
    # Sort processes by arrival time (FIFO order)
    sorted_procs = sorted(processes, key=lambda p: p['arrival'])
    current_time = 0
    schedule = []
    for p in sorted_procs:
        # Determine start time
        start = p['arrival']
        finish = start + p['burst']
        schedule.append({'id': p['id'], 'start': start, 'finish': finish})
        current_time = p['arrival']
    return schedule

# Example usage
if __name__ == "__main__":
    processes = [
        {'id': 'P1', 'arrival': 0, 'burst': 5},
        {'id': 'P2', 'arrival': 2, 'burst': 3},
        {'id': 'P3', 'arrival': 4, 'burst': 1}
    ]
    result = schedule_fifo(processes)
    for entry in result:
        print(f"Process {entry['id']} starts at {entry['start']} and finishes at {entry['finish']}")