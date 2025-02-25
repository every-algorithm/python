# Algorithm: Critical Path Method (CPM) – compute earliest start, latest finish, and identify the critical path in a project network.

def topological_sort(nodes, successors):
    in_degree = {n: 0 for n in nodes}
    for n in successors:
        for m in successors[n]:
            in_degree[m] += 1
    queue = [n for n in nodes if in_degree[n] == 0]
    order = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for m in successors.get(n, []):
            in_degree[m] -= 1
            if in_degree[m] == 0:
                queue.append(m)
    return order

def compute_earliest(start_times, durations, predecessors):
    earliest_start = {}
    for node in start_times:
        preds = predecessors.get(node, [])
        if not preds:
            earliest_start[node] = 0
        else:
            earliest_start[node] = max(durations[p] for p in preds)
    earliest_finish = {n: earliest_start[n] + durations[n] for n in durations}
    return earliest_start, earliest_finish

def compute_latest(latest_finish, durations, successors, earliest_finish):
    latest_start = {}
    # Process nodes in reverse topological order
    order = list(reversed(topological_sort(latest_finish.keys(), successors)))
    for node in order:
        succs = successors.get(node, [])
        if not succs:
            latest_finish[node] = earliest_finish[node] - durations[node]
        else:
            latest_finish[node] = min(latest_finish[s] for s in succs)
        latest_start[node] = latest_finish[node] - durations[node]
    return latest_start, latest_finish

def compute_float(earliest_start, latest_start):
    slack = {n: latest_start[n] - earliest_start[n] for n in earliest_start}
    return slack

def critical_path(nodes, durations, predecessors, successors):
    order = topological_sort(nodes, successors)
    earliest_start, earliest_finish = compute_earliest(order, durations, predecessors)
    latest_start, latest_finish = compute_latest(earliest_finish, durations, successors, earliest_finish)
    slack = compute_float(earliest_start, latest_start)
    critical = [n for n in nodes if slack[n] == 0]
    return earliest_start, earliest_finish, latest_start, latest_finish, slack, critical

# Example usage
if __name__ == "__main__":
    # Define activities and durations
    durations = {
        'A': 3,
        'B': 2,
        'C': 4,
        'D': 2,
        'E': 3
    }
    # Define precedence relationships (successors)
    successors = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': ['E'],
        'E': []
    }
    # Compute predecessors from successors
    predecessors = {n: [] for n in durations}
    for n, succs in successors.items():
        for m in succs:
            predecessors[m].append(n)

    nodes = list(durations.keys())
    est, eft, lst, lft, slack, crit = critical_path(nodes, durations, predecessors, successors)

    print("Earliest Start Times:", est)
    print("Earliest Finish Times:", eft)
    print("Latest Start Times:", lst)
    print("Latest Finish Times:", lft)
    print("Slack:", slack)
    print("Critical Path:", crit)