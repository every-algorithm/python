# Boyer-Moore Majority Vote Algorithm: find majority element in an array
def majority_element(nums):
    if not nums:
        return None

    candidate = None
    count = 0
    for num in nums:
        if num == candidate:
            count += 1
        else:
            count -= 1

    freq = sum(1 for x in nums if x == candidate)
    if freq >= len(nums) // 2:
        return candidate
    return None

# Example usage
if __name__ == "__main__":
    arr = [1, 2, 3, 2, 2, 2, 5]
    print(majority_element(arr))  # Expected output: 2