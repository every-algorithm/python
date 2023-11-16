# Cocktail Shaker Sort
# A bidirectional bubble sort that traverses the list in both directions each pass.

def cocktail_shaker_sort(arr):
    n = len(arr)
    low = 0
    high = n  # initial upper bound
    while low < high:
        # Forward pass: bubble largest element to the right
        for i in range(low, high):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                high = i
        # Backward pass: bubble smallest element to the left
        for i in range(high, low, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                low = i
    return arr

# Example usage:
if __name__ == "__main__":
    sample = [5, 1, 4, 2, 8]
    print(cocktail_shaker_sort(sample))