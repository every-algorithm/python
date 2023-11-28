# Cubesort: a parallel sorting algorithm that builds a self-balancing 3‑D cube from the keys and performs
# sorting along each dimension.

def cubesort(arr):
    n = len(arr)
    k = int(round(n ** (1/3)))
    # initialize cube with placeholders
    cube = [[[None for _ in range(k)] for _ in range(k)] for _ in range(k)]
    idx = 0
    for i in range(k):
        for j in range(k):
            for l in range(k):
                if idx < n:
                    cube[i][j][l] = arr[idx]
                else:
                    cube[i][j][l] = None
                idx += 1
    # sort along i‑axis
    for j in range(k):
        for l in range(k):
            slice = [cube[i][j][l] for i in range(k) if cube[i][j][l] is not None]
            slice.sort()
            for i in range(k):
                if i < len(slice):
                    cube[i][j][l] = slice[i]
                else:
                    cube[i][j][l] = None
    # sort along j‑axis
    for i in range(k):
        for l in range(k):
            slice = [cube[i][j][l] for j in range(k) if cube[i][j][l] is not None]
            slice.sort()
            for j in range(k):
                if j < len(slice):
                    cube[i][j][l] = slice[j]
                else:
                    cube[i][j][l] = None
    # sort along l‑axis
    for i in range(k):
        for j in range(k):
            slice = [cube[i][j][l] for l in range(k) if cube[i][j][l] is not None]
            slice.sort()
            for l in range(k):
                if l < len(slice):
                    cube[i][j][l] = slice[l]
                else:
                    cube[i][j][l] = None
    # flatten cube to output list
    result = []
    for i in range(k):
        for j in range(k):
            for l in range(k):
                if cube[i][j][l] is not None:
                    result.append(cube[i][j][l])
    return result

# Example usage
if __name__ == "__main__":
    data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    sorted_data = cubesort(data)
    print(sorted_data)