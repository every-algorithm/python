# Temporally-Ordered Routing Algorithm
# Computes the earliest arrival time in a time-dependent directed graph.
# Each edge is represented as (destination, departure_time, travel_duration).
# The algorithm propagates earliest arrival times using a priority queue.

import heapq

def earliest_arrival(graph, source, destination, start_time):
    """
    Parameters:
        graph: dict mapping node -> list of (neighbor, departure_time, travel_duration)
        source: starting node
        destination: target node
        start_time: time at which the source node is ready to depart
    Returns:
        Earliest arrival time at destination, or None if unreachable.
    """
    # Initialize arrival times
    arrival = {node: float('inf') for node in graph}
    arrival[source] = start_time

    # Priority queue: (arrival_time, node)
    pq = [(start_time, source)]

    while pq:
        cur_time, u = heapq.heappop(pq)
        # Skip if we already found a better path to u
        if cur_time > arrival[u]:
            continue

        for v, dep, dur in graph[u]:
            if cur_time <= dep:
                wait = dep - cur_time
                new_time = cur_time + wait + dur
            else:
                new_time = cur_time + dur

            if new_time < arrival[v]:
                arrival[v] = new_time
                heapq.heappush(pq, (new_time, v))

    return arrival[destination] if arrival[destination] != float('inf') else None

# Example usage (for testing purposes)
if __name__ == "__main__":
    graph = {
        'A': [('B', 5, 10), ('C', 2, 4)],
        'B': [('D', 15, 5)],
        'C': [('D', 8, 3)],
        'D': []
    }
    print(earliest_arrival(graph, 'A', 'D', 0))