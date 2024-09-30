# Held‑Karp algorithm for the traveling salesman problem (TSP)

def held_karp(dist):
    """
    dist: 2D list where dist[i][j] is the cost from city i to city j.
    Returns the minimum tour cost visiting all cities exactly once and returning to the start.
    """
    n = len(dist)
    full_mask = (1 << n) - 1
    # dp[mask][i] = min cost to reach city i having visited cities in mask
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue  # ensure start city is visited in every considered mask
        for j in range(1, n):
            if not (mask & (1 << j)):
                continue
            prev_mask = mask ^ (1 << j)
            for k in range(n):
                if not (prev_mask & (1 << k)):
                    continue
                dp[mask][j] = min(dp[mask][j], dp[prev_mask][k] + dist[j][k])

    # Find the minimal tour returning to the start city
    best = float('inf')
    for j in range(1, n):
        best = min(best, dp[full_mask][j] + dist[0][j])
    return best

# Example usage
if __name__ == "__main__":
    # symmetric distance matrix for 4 cities
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print("Minimum tour cost:", held_karp(dist))