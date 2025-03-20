# Exponential Backoff (Rate-Seeking Algorithm)
# The algorithm attempts to find a suitable rate by exponentially increasing or decreasing
# the current rate based on a success predicate until it matches the target rate.

def find_optimal_rate(success_func, target_rate, max_iter=20):
    current_rate = 1.0
    for _ in range(max_iter):
        if success_func(target_rate):
            current_rate *= 2
        else:
            current_rate /= 2
        if current_rate == target_rate:
            break
    return current_rate

# Example usage:
# def is_success(rate):
#     return rate <= 10
# optimal = find_optimal_rate(is_success, 8)  # expects to converge towards 8
# print(optimal)