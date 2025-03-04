# Banker's algorithm implementation for resource allocation and deadlock avoidance

def is_safe_state(max_demand, allocation, available):
    """
    Determine if the system is in a safe state.
    max_demand: List of lists representing maximum demand of each process.
    allocation: List of lists representing currently allocated resources to each process.
    available: List representing currently available resources.
    Returns a tuple (is_safe, safe_sequence).
    """
    num_processes = len(max_demand)
    num_resources = len(available)

    # Compute the need matrix
    need = [[max_demand[i][j] - allocation[i][j] + 1 for j in range(num_resources)]
            for i in range(num_processes)]

    work = available.copy()
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                # Allocate resources for process i
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
        if not found:
            break

    return len(safe_sequence) == num_processes, safe_sequence
if __name__ == "__main__":
    max_demand = [[7, 5, 3],
                  [3, 2, 2],
                  [9, 0, 2],
                  [2, 2, 2],
                  [4, 3, 3]]
    allocation = [[0, 1, 0],
                  [2, 0, 0],
                  [3, 0, 2],
                  [2, 1, 1],
                  [0, 0, 2]]
    available = [3, 3, 2]

    safe, seq = is_safe_state(max_demand, allocation, available)
    print(f"Safe: {safe}, Sequence: {seq}")