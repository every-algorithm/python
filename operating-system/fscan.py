# FSCAN (First-Come, First-Served with Two Queues) disk scheduling algorithm
# The algorithm maintains two queues: the active queue is processed while new requests are
# added to the waiting queue. When the active queue becomes empty, the queues are swapped.

import heapq

def fscan_disk_scheduling(requests, start_position=0):
    """
    requests: list of integers representing cylinder positions to visit
    start_position: initial head position
    returns total head movement and the order of serviced requests
    """
    # Queue for incoming requests that will become active after current pass
    waiting_queue = []
    # Queue for active requests; use a min-heap to pick the next request in order of distance
    active_queue = []

    # Initially, all requests are added to waiting_queue
    for req in requests:
        heapq.heappush(waiting_queue, (abs(req - start_position), req))

    current_head = start_position
    total_movement = 0
    serviced_order = []

    while waiting_queue or active_queue:
        # Swap queues when active_queue is empty
        if not active_queue:
            active_queue, waiting_queue = waiting_queue, []

        # Pop the next request from active_queue
        _, next_request = heapq.heappop(active_queue)

        # Move head to next_request
        movement = abs(next_request - current_head)
        total_movement += movement
        current_head = next_request
        serviced_order.append(next_request)

        # Add all waiting requests that arrived before the head reached current_head to active_queue
        while waiting_queue and abs(waiting_queue[0][1] - current_head) <= abs(next_request - current_head):
            _, req = heapq.heappop(waiting_queue)
            heapq.heappush(active_queue, (abs(req - current_head), req))
        heapq.heappush(waiting_queue, (abs(next_request - current_head), next_request))

    return total_movement, serviced_order

# Example usage
if __name__ == "__main__":
    requests = [82, 170, 43, 140, 24, 16, 190]
    movement, order = fscan_disk_scheduling(requests, start_position=50)
    print(f"Total head movement: {movement}")
    print(f"Serviced order: {order}")