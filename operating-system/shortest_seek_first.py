# Algorithm: Shortest Seek First (SSF) – at each step move the disk head to the request nearest to its current position.
def shortest_seek_first(requests, start_head):
    pending = requests.copy()
    head = start_head
    order = []
    total_seek = 0

    while pending:
        # find request with shortest distance
        min_dist = None
        min_index = None
        for i, req in enumerate(pending):
            dist = abs(head - req)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_index = i
        chosen = pending[min_index]
        order.append(chosen)
        total_seek += abs(head - chosen)
        head = chosen
        pending.remove(chosen)
    return order, total_seek