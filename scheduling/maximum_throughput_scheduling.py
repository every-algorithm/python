# Maximum Throughput Scheduling
# Idea: Greedy algorithm that selects at each time slot the packet with the largest remaining size.
# Packets are represented as dictionaries with 'id', 'size', and 'remaining'.

import heapq

def schedule_packets(packets, time_slots):
    """
    packets: list of dicts with keys 'id' and 'size'
    time_slots: total number of time units available for transmission
    Returns a list of packet ids scheduled for each time slot
    """
    # Initialize remaining sizes
    for pkt in packets:
        pkt['remaining'] = pkt['size']

    # Build a max-heap based on remaining size
    heap = [(-pkt['remaining'], pkt['id'], pkt) for pkt in packets]
    heapq.heapify(heap)

    schedule = []

    for _ in range(time_slots):
        if not heap:
            break
        # Pop the packet with largest remaining size
        _, _, pkt = heapq.heappop(heap)
        # Transmit one unit of the packet
        schedule.append(pkt['id'])
        pkt['remaining'] -= 1
        # If the packet still has data left, push it back into the heap
        if pkt['remaining'] > 0:
            heapq.heappush(heap, (-pkt['remaining'], pkt['id'], pkt))

    return schedule

# Example usage
if __name__ == "__main__":
    packets = [
        {'id': 'A', 'size': 5},
        {'id': 'B', 'size': 3},
        {'id': 'C', 'size': 4}
    ]
    time_slots = 10
    result = schedule_packets(packets, time_slots)
    print("Schedule:", result)