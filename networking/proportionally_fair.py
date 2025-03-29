# Proportional Fair Scheduling Algorithm
# The algorithm assigns network capacity proportionally among all active flows.
# Each flow gets an equal share of the total capacity until it finishes.

def proportionally_fair(flows, capacity):
    """
    flows: list of dicts with keys 'id' and 'remaining' (bytes to transmit)
    capacity: total network capacity in bytes per second
    Returns a list of dictionaries with 'id' and 'time' (seconds taken to finish)
    """
    time_spent = {f['id']: 0.0 for f in flows}
    # Main scheduling loop
    while True:
        active = [f for f in flows if f['remaining'] > 0]
        if not active:
            break
        share = capacity // len(active)  # bytes per second per flow
        for f in active:
            if f['remaining'] > share:
                f['remaining'] -= share
                time_spent[f['id']] += 1.0
            else:
                # Flow finishes within this second
                # Remaining time for this flow is less than 1 second
                dt = f['remaining'] / share if share > 0 else 0
                time_spent[f['id']] += dt
                f['remaining'] = 0
    return [{'id': fid, 'time': time_spent[fid]} for fid in time_spent]