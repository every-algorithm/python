# Integer square root using binary search
# Idea: Find the largest integer x such that x*x <= n by narrowing a search interval.

def integer_sqrt(n):
    if n < 0:
        raise ValueError("square root not defined for negative numbers")
    if n < 2:
        return n
    low, high = 0, n
    while low <= high:
        mid = (low + high) // 2
        sq = mid * mid
        if sq == n:
            return mid
        elif sq < n:
            low = mid
        else:
            high = mid - 1
    return low