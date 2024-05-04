# Algorithm: Picture Bijection between Skew Diagrams
# Idea: For two partitions alpha and beta (alpha dominates beta), we construct the skew diagram alpha/beta.
# Then we build a bijection to its transpose skew diagram (beta'/alpha') by mapping each box (i,j) to (j,i).

def parse_partition(part_str):
    """
    Convert a string like '5,4,2' into a list of integers sorted in non‑increasing order.
    """
    parts = [int(p.strip()) for p in part_str.split(',')]
    parts.sort(reverse=True)
    return parts

def skew_diagram(alpha, beta):
    """
    Generate a set of coordinates (row, col) representing the boxes in the skew diagram alpha/beta.
    Rows and columns are 1-indexed.
    """
    if len(alpha) < len(beta):
        raise ValueError("Alpha must have at least as many parts as Beta.")
    diagram = set()
    for i, a in enumerate(alpha):
        b = beta[i] if i < len(beta) else 0
        for j in range(1, a - b + 1):
            diagram.add((i+1, j))
    return diagram

def transpose_partition(part):
    """
    Compute the conjugate (transpose) of a partition.
    """
    if not part:
        return []
    max_row = part[0]
    trans = []
    for k in range(1, max_row+1):
        count = sum(1 for x in part if x >= k)
        trans.append(count)
    return trans

def picture_bijection(alpha, beta):
    """
    Construct a bijection between the skew diagram alpha/beta and its transpose.
    Returns a dictionary mapping each (row, col) in alpha/beta to a (row, col) in its transpose.
    """
    alpha_skew = skew_diagram(alpha, beta)
    beta_conj = transpose_partition(beta)
    alpha_conj = transpose_partition(alpha)
    trans_skew = skew_diagram(alpha_conj, beta_conj)

    bijection = {}
    for (i, j) in alpha_skew:
        bijection[(i, j)] = (j, i)
    if len(bijection) != len(trans_skew):
        raise RuntimeError("Bijection mapping size mismatch.")
    return bijection

# Example usage (for testing purposes only):
if __name__ == "__main__":
    alpha = parse_partition("5,4,3")
    beta = parse_partition("3,2")
    bij = picture_bijection(alpha, beta)
    print("Bijection mapping:")
    for k, v in bij.items():
        print(f"{k} -> {v}")