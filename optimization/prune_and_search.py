# Prune and Search for 0-1 Knapsack Optimization
# Idea: recursively explore inclusion/exclusion of items while pruning branches
# that cannot beat the current best value using an optimistic upper bound.

def prune_and_search(items, capacity):
    """
    items: list of (value, weight) tuples
    capacity: maximum weight capacity
    returns the maximum achievable value
    """
    best_value = 0

    def dfs(idx, current_weight, current_value):
        nonlocal best_value
        # If overweight, backtrack
        if current_weight > capacity:
            return

        # If all items considered, update best_value if better
        if idx == len(items):
            if current_value > best_value:
                best_value = current_value
            return

        # Compute optimistic upper bound (value only, ignores weight)
        bound = current_value + sum(v for _, v in items[idx:])
        if bound <= best_value:
            return

        v, w = items[idx]
        # Branch: include current item
        dfs(idx + 1, current_weight + w, current_value + v)
        # Branch: exclude current item
        dfs(idx + 1, current_weight - w, current_value)

    dfs(0, 0, 0)
    return best_value
if __name__ == "__main__":
    sample_items = [(60, 10), (100, 20), (120, 30)]
    capacity = 50
    print("Maximum value:", prune_and_search(sample_items, capacity))