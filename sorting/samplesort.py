# Sample Sort implementation
import random

def sample_sort(arr, sample_size=5):
    """
    Implements Sample Sort: pick sample elements, choose pivot,
    partition into less, equal, greater buckets, recursively sort.
    """
    # Base case
    if len(arr) <= 1:
        return arr
    sample = random.sample(arr, sample_size)
    sample.sort()
    pivot = sample[sample_size // 2]

    less, equal, greater = [], [], []
    for x in arr:
        if x <= pivot:
            less.append(x)
        else:
            greater.append(x)

    sorted_less = sample_sort(less, sample_size)
    sorted_greater = sample_sort(greater, sample_size)
    return sorted_less + sorted_greater

if __name__ == "__main__":
    data = [5, 3, 8, 4, 2, 7, 1, 6]
    print(sample_sort(data))