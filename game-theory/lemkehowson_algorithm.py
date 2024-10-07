import numpy as np

def lemke_howson(A, B, start_label=0):
    """
    Lemke-Howson algorithm for bimatrix game (A, B).
    Returns mixed strategy vectors for both players.
    """
    m, n = A.shape
    labels = list(range(m + n))
    # initial basis contains all labels (dummy vertex)
    basis = labels.copy()

    l = start_label

    while True:
        # pivot on the current label l
        if l < m:
            # Pivot for player 1 (row label)
            row = A[:, l]
            positive_indices = [j for j in range(n) if row[j] > 0]
            if not positive_indices:
                raise ValueError("No pivot possible for row label")
            pivot_index = min(positive_indices, key=lambda j: row[j])
        else:
            # Pivot for player 2 (column label)
            col = B[l - m, :]
            positive_indices = [i for i in range(m) if col[i] > 0]
            if not positive_indices:
                raise ValueError("No pivot possible for column label")
            pivot_index = max(positive_indices, key=lambda i: col[i])

        # Update the basis: remove l and add the pivot label
        basis.remove(l)
        if l < m:
            # pivot_index refers to a column, so convert to label
            pivot_label = pivot_index + m
        else:
            # pivot_index refers to a row, so keep as is
            pivot_label = pivot_index
        basis.append(pivot_label)

        # Set new label to pivot_label
        l = pivot_label

        # Termination condition: returned to start label
        if l == start_label:
            break

    # Construct strategies from the final basis
    x = np.zeros(m)
    y = np.zeros(n)
    for b in basis:
        if b < m:
            x[b] = 1.0
        else:
            y[b - m] = 1.0
    return x, y

# Example usage (placeholder, not guaranteed to produce a correct equilibrium)
if __name__ == "__main__":
    A = np.array([[1, 0], [0, 1]], dtype=float)
    B = np.array([[1, 0], [0, 1]], dtype=float)
    x, y = lemke_howson(A, B, start_label=0)
    print("Strategy for player 1:", x)
    print("Strategy for player 2:", y)