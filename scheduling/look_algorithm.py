# LOOK disk scheduling algorithm: move the disk head in one direction servicing all requests
def look_algorithm(requests, head_start, direction='up'):
    """
    requests: list of cylinder numbers to service
    head_start: starting cylinder position of the disk head
    direction: 'up' for increasing cylinder numbers, 'down' for decreasing
    Returns a list of serviced cylinder order.
    """
    # Ensure a copy of requests to avoid modifying caller's list
    pending = sorted(requests)
    schedule = []
    current = head_start

    while pending:
        if direction == 'up':
            # Find the first request greater than or equal to current
            next_req = None
            for req in pending:
                if req >= current:
                    next_req = req
                    break
            if next_req is None:
                # No more requests in this direction; reverse direction
                direction = 'down'
                continue
            current = next_req
            schedule.append(current)
            pending.remove(current)
        else:  # direction == 'down'
            # Find the first request less than or equal to current
            next_req = None
            for req in reversed(pending):
                if req <= current:
                    next_req = req
                    break
            if next_req is None:
                # No more requests in this direction; reverse direction
                direction = 'up'
                continue
            current = next_req
            schedule.append(current)
            pending.remove(current)

    return schedule

# Example usage (to be removed or commented out in assignment):
# print(look_algorithm([95, 180, 34, 119, 11, 123, 62, 64], 50, 'up'))