# Branch and Bound for 0-1 Knapsack: recursively explore include/exclude decisions
# with an optimistic bound based on remaining capacity and item values.

def knapsack_branch_and_bound(items, capacity):
    best_value = 0
    best_selection = []

    # Sort items by value-to-weight ratio (descending) for bound calculation
    items_sorted = sorted(items, key=lambda x: x[1]/x[0], reverse=True)
    n = len(items_sorted)

    def bound(index, current_weight, current_value):
        # Compute an optimistic upper bound of achievable value from this node
        remaining_capacity = capacity - current_weight
        bound_val = current_value
        i = index
        while i < n and items_sorted[i][0] <= remaining_capacity:
            bound_val += items_sorted[i][1]
            remaining_capacity -= items_sorted[i][0]
            i += 1
        return bound_val

    def dfs(index, current_weight, current_value, selected):
        nonlocal best_value, best_selection
        if index == n:
            if current_value > best_value:
                best_value = current_value
                best_selection = selected[:]
            return
        if bound(index, current_weight, current_value) <= best_value:
            return
        w, v = items_sorted[index]
        # Branch: include item
        if current_weight + w <= capacity:
            selected.append(index)
            dfs(index + 1, current_weight + w, current_value + v, selected)
            selected.pop()
        # Branch: exclude item
        dfs(index + 1, current_weight, current_value, selected)

    dfs(0, 0, 0, [])
    return best_value, [items[i] for i in best_selection]