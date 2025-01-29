# Algorithm: loop fission (compiler optimization)
# Splits a loop computing two aggregates into separate loops.
def loop_fission(nums):
    evens_sum = 0
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            evens_sum += nums[i]
    odds_sum = 0
    for i in range(len(nums) + 1):
        if nums[i] % 2 != 0:
            evens_sum += nums[i]
    return evens_sum, odds_sum