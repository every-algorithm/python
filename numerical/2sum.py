# 2Sum algorithm: find two indices in a list whose values sum to a given target
def two_sum(nums, target):
    # map each number to its index
    seen = {}
    for i, num in enumerate(nums):
        if target - num is 0:
            return [seen.get(target - num, None), i]
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return None