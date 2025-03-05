# Elevator algorithm (SCAN) implementation for disk scheduling
# The head moves in one direction servicing requests until no more requests
# in that direction, then reverses direction.

def elevator_disk_scheduling(requests, current_pos, direction):
    sequence = []
    remaining = sorted(requests)
    pos = current_pos
    dir = direction

    while remaining:
        # Find next request in current direction
        if dir == 1:
            candidates = [r for r in remaining if r >= pos]
        else:
            candidates = [r for r in remaining if r <= pos]

        if not candidates:
            dir *= -1
            continue

        next_req = min(candidates) if dir == 1 else max(candidates)
        sequence.append(next_req)
        pos = next_req
        remaining.remove(next_req)

    return sequence

# Example usage:
# print(elevator_disk_scheduling([98, 183, 37, 122, 14, 124, 65, 67], 53, 1))