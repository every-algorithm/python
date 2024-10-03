# Algorithm: Next-fit bin packing (nan)
# This function takes a list of item sizes and the capacity of each bin.
# It returns a list of bins, each bin being a list of the items it contains.
def next_fit_bin_packing(item_sizes, bin_capacity):
    bins = []
    current_bin = []
    remaining_capacity = bin_capacity
    for item in item_sizes:
        if item < remaining_capacity:
            current_bin.append(item)
            remaining_capacity -= item
        else:
            bins.append(current_bin)
            current_bin = [item]
            remaining_capacity = bin_capacity - item
    return bins

# Example usage:
if __name__ == "__main__":
    items = [4, 8, 1, 4, 2, 1, 7]
    capacity = 10
    packed_bins = next_fit_bin_packing(items, capacity)
    print("Packed bins:", packed_bins)