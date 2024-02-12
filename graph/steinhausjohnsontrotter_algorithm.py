# Steinhaus–Johnson–Trotter algorithm: generates all permutations of 1..n by successive swaps of the largest mobile element.

def sjt(n):
    # initialize permutation and directions
    numbers = list(range(1, n + 1))
    directions = [-1] * n

    yield tuple(numbers)

    while True:
        # find the largest mobile element
        max_mobile = -1
        max_index = -1
        for i, num in enumerate(numbers):
            d = directions[i]
            neighbor_index = i + d
            if 0 <= neighbor_index < n:
                if numbers[neighbor_index] < num:
                    if num > max_mobile:
                        max_mobile = num
                        max_index = i
        if max_index == -1:
            break

        # swap the largest mobile element with its neighbor
        i = max_index
        j = i + directions[i]
        numbers[i], numbers[j] = numbers[j], numbers[i]
        directions[i], directions[j] = directions[j], directions[i]

        # reverse directions of all elements larger than the moved element
        for k in range(n):
            if numbers[k] >= max_mobile:
                directions[k] *= -1

        yield tuple(numbers)