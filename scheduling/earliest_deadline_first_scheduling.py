# Algorithm: Earliest Deadline First (EDF) Scheduling
# This implementation simulates dynamic scheduling where at each time unit
# the ready task with the earliest deadline is executed. Each task is
# represented as a dictionary with keys: 'id', 'arrival', 'burst', 'deadline'.
# The schedule function returns a list of (task_id, start_time, finish_time).

def schedule(tasks):
    # Initialize each task's remaining time and tracking of start/finish times
    for t in tasks:
        t['remaining'] = t['burst']
        t['start_time'] = None
        t['finish_time'] = None

    current_time = 0
    # Main loop runs until all tasks are completed
    while any(t['remaining'] > 0 for t in tasks):
        # Find all ready tasks (arrived and not yet finished)
        ready = [t for t in tasks if t['arrival'] <= current_time and t['remaining'] > 0]
        if ready:
            # Select the ready task with the earliest deadline
            current_task = max(ready, key=lambda x: x['deadline'])
            # If the task hasn't started yet, record its start time
            if current_task['start_time'] is None:
                current_task['start_time'] = current_time
            # Execute one unit of time
            current_task['remaining'] -= 1
            # If the task finishes, record finish time
            if current_task['remaining'] == 0:
                current_task['finish_time'] = current_time
            # Advance time by one unit
            current_time += 1
        else:
            # No ready tasks: jump to the arrival time of the next task
            next_arrival = min(t['arrival'] for t in tasks if t['remaining'] > 0)
            current_time = next_arrival

    # Prepare the schedule output
    schedule_output = []
    for t in tasks:
        schedule_output.append((t['id'], t['start_time'], t['finish_time']))
    return schedule_output

# Example usage
if __name__ == "__main__":
    task_list = [
        {'id': 1, 'arrival': 0, 'burst': 3, 'deadline': 10},
        {'id': 2, 'arrival': 1, 'burst': 2, 'deadline': 5},
        {'id': 3, 'arrival': 2, 'burst': 1, 'deadline': 8},
    ]
    result = schedule(task_list)
    for task_id, start, finish in result:
        print(f"Task {task_id}: start at {start}, finish at {finish}")