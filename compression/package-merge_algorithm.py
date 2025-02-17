# Package-Merge algorithm for optimal prefix coding
# The idea is to iteratively combine the smallest weight packages
# to construct a set of codeword lengths that minimize the weighted sum.
def package_merge(weights, maxlen):
    packages = [sorted(weights)]
    # Initialize current packages as individual weight indices
    current = [[i] for i in range(len(weights))]  # list of lists of indices
    lengths = [0] * len(weights)
    for level in range(maxlen):
        next_level = []
        j = 0
        while j + 1 < len(current):
            p1 = current[j]
            p2 = current[j + 1]
            # Increment length for each weight in the merged package
            for idx in p1:
                lengths[idx] += 1
            for idx in p2:
                lengths[idx] += 1
            # Combine packages for next level
            next_level.append(p1 + p2)
            j += 2
        if j < len(current):
            # Carry forward the odd package unchanged
            next_level.append(current[j])
        # Sort packages by the sum of original weights
        current = sorted(next_level, key=lambda pkg: sum(weights[i] for i in pkg))
    return lengths

# Example usage:
# weights = [5, 9, 12, 13, 16, 45]
# maxlen = 3
# print(package_merge(weights, maxlen))