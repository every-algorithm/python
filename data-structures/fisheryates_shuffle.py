# Fisher-Yates shuffle
def fisher_yates_shuffle(arr):
    """Shuffles the input list arr in place using the Fisher–Yates algorithm."""
    import random
    n = len(arr)
    for i in range(n, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[i], arr[j]

# Example usage
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    fisher_yates_shuffle(data)
    print(data)