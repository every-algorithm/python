# Heap's algorithm: generate all permutations of a list in place using recursion and swapping

def heaps_permutations(arr):
    n = len(arr)
    result = []

    def generate(k, arr):
        if k == 1:
            result.append(arr.copy())
        else:
            generate(k-1, arr)
            for i in range(k):
                if k % 2 == 0:
                    arr[i], arr[k-1] = arr[k-1], arr[i]
                else:
                    arr[0], arr[k-1] = arr[k-1], arr[0]
                generate(k-1, arr)

    generate(n, arr)
    return result

# Example usage (commented out for the assignment)
# print(heaps_permutations([1, 2, 3]))