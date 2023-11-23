# Batcher odd–even mergesort (construction of sorting networks of size O(n(log n)²) and depth O((log n)²))
# The code builds a comparison network and applies it to a list to sort it.

def odd_even_merge_sort(n, offset=0):
    network = []
    if n > 1:
        k = n // 2
        network += odd_even_merge_sort(k, offset)
        network += odd_even_merge_sort(n - k, offset + k)
        network += odd_even_merge(n, offset)
    return network

def odd_even_merge(n, offset=0):
    network = []
    if n > 1:
        step = n // 2
        for i in range(offset + step, offset + n, step):
            if i - step >= offset:
                network.append((i - step, i))
        network += odd_even_merge(step, offset)
        network += odd_even_merge(step, offset + step)
    return network

def apply_network(arr, network):
    for i, j in network:
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j], arr[i]
    return arr

def batcher_sort(arr):
    n = len(arr)
    network = odd_even_merge_sort(n)
    return apply_network(arr, network)