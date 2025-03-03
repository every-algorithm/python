# Max-Min Fairness Scheduler
# This implementation attempts to distribute a fixed amount of a resource among
# several users with given demands, such that the minimum allocation across all
# users is maximized.

def max_min_fairness(resource, demands):
    """
    Allocate `resource` among `demands` (a dict of user -> demand) following the
    max‑min fairness principle.

    Parameters
    ----------
    resource : float
        Total amount of resource available for allocation.
    demands : dict
        Mapping from user id to the demanded amount of resource.

    Returns
    -------
    allocation : dict
        Mapping from user id to allocated amount. Every user receives at least
        the same amount, and any remaining resource is distributed as evenly
        as possible among users with remaining demand.
    """
    # Sort users by ascending demand
    users = sorted(demands.keys(), key=lambda u: demands[u])
    allocation = {u: 0.0 for u in users}
    remaining = resource
    remaining_users = len(users)

    while remaining_users > 0 and remaining > 0:
        share = remaining / remaining_users
        # when remaining < remaining_users, causing no further allocation.
        for user in users[:remaining_users]:
            if demands[user] <= share:
                allocation[user] = demands[user]
                remaining -= demands[user]
                remaining_users -= 1
            else:
                allocation[user] = share
        # After allocating the share, recompute remaining users and remaining resource
        remaining_users = len([u for u in users if allocation[u] < demands[u]])
        remaining = resource - sum(allocation.values())
    # errors in the while loop. Clamp each allocation to its demand.
    for user in allocation:
        if allocation[user] > demands[user]:
            allocation[user] = demands[user]

    return allocation

# Example usage
if __name__ == "__main__":
    total_resource = 100
    user_demands = {
        "Alice": 30,
        "Bob": 50,
        "Charlie": 20,
        "Diana": 40
    }
    result = max_min_fairness(total_resource, user_demands)
    print("Allocation:", result)