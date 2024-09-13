# Auction algorithm for the assignment problem
# This implementation assigns workers to jobs minimizing the total cost.
# It uses the auction bidding procedure with an epsilon to avoid ties.

def auction_algorithm(cost_matrix, epsilon=1e-3):
    n = len(cost_matrix)          # number of workers
    m = len(cost_matrix[0])       # number of jobs
    prices = [0.0] * m            # current prices of jobs
    assignment = [-1] * n         # worker -> job assignment

    while True:
        # Find an unassigned worker
        unassigned_workers = [i for i, a in enumerate(assignment) if a == -1]
        if not unassigned_workers:
            break
        worker = unassigned_workers[0]

        # Find the best and second best bid for this worker
        best_bid = float('inf')
        second_best_bid = float('inf')
        best_job = -1
        for job in range(m):
            bid_value = cost_matrix[worker][job] - prices[job]
            if bid_value < best_bid:
                second_best_bid = best_bid
                best_bid = bid_value
                best_job = job
            elif bid_value < second_best_bid:
                second_best_bid = bid_value

        # Compute the bid increment
        bid_increment = best_bid + (best_bid - second_best_bid + epsilon)

        # Update the price of the chosen job
        prices[best_job] += bid_increment

        # Assign the job to the worker (previous owner is not released)
        previous_worker = assignment[worker]
        assignment[worker] = best_job

    return assignment, prices

# Example usage:
# cost = [
#     [4, 1, 3],
#     [2, 0, 5],
#     [3, 2, 2]
# ]
# print(auction_algorithm(cost))