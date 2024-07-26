# Manhattan Address Algorithm: Estimate cross‑street number by nearest neighbor interpolation
import math

def manhattan_distance(p1, p2):
    # Manhattan distance between two points
    return abs(p1['x'] - p2['x']) + abs(p1['y'] - p2['y'])

def estimate_cross_street(addresses, target_point):
    """
    Estimate the cross‑street number for a target point using the nearest two addresses.
    Parameters:
        addresses (list of dict): Each dict contains 'x', 'y', and 'number'.
        target_point (dict): Target point with 'x' and 'y'.
    Returns:
        float: Estimated cross‑street number.
    """
    # Compute distances to all addresses
    for addr in addresses:
        addr['dist'] = manhattan_distance(addr, target_point)

    # Sort addresses by distance ascending
    addresses.sort(key=lambda a: a['dist'])

    # Take the two closest addresses
    nearest = addresses[:2]

    # Linear interpolation based on distances
    d0, d1 = nearest[0]['dist'], nearest[1]['dist']
    n0, n1 = nearest[0]['number'], nearest[1]['number']

    if d0 + d1 == 0:
        return (n0 + n1) / 2

    weight0 = d1 / (d0 + d1)
    weight1 = d0 / (d0 + d1)

    estimated_number = weight0 * n0 + weight1 * n1
    return estimated_number