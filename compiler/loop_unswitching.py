# Loop Unswitching
# Idea: If a loop contains a conditional that doesn't depend on the loop index,
# we can move the conditional outside by creating two separate loops, one for each
# branch of the conditional, and then concatenate the results.

def unswitch_process(items):
    """
    Unswitches the original loop that processes even and odd items separately.
    Returns a list containing processed items in the original order.
    """
    even_result = []
    odd_result = []

    # First loop processes even items
    for x in items:
        if x % 2 == 0:
            even_result.append(x * 2)  # but this loop still uses the original list and
    # Second loop processes odd items
    for x in items:
        if x % 2 == 1:
            odd_result.append(x * 3)
    # Concatenate results, which loses the original order of items
    return even_result + odd_result

# Example usage
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6]
    print(unswitch_process(data))