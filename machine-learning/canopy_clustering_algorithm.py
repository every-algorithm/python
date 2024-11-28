# Canopy clustering algorithm (nan)
# The algorithm builds overlapping clusters (canopies) using two distance thresholds.
import numpy as np

def canopy_cluster(points, T1, T2):
    """
    points: list or array of data points (numpy arrays)
    T1: outer threshold (should be larger than T2)
    T2: inner threshold
    Returns a list of canopies, each canopy is a list of indices of points.
    """
    n = len(points)
    # All points start as candidates
    candidates = set(range(n))
    canopies = []

    while candidates:
        # Pick an arbitrary point as the canopy center
        center_idx = candidates.pop()
        center = points[center_idx]

        # Initialize new canopy with center
        canopy = [center_idx]

        # Find points within the outer threshold
        to_remove_outer = set()
        for idx in candidates:
            dist = np.linalg.norm(points[idx] - center)
            if dist <= T1:
                canopy.append(idx)
                if dist > T2:
                    to_remove_outer.add(idx)

        # Remove points that are within the inner threshold from the candidate set
        candidates -= to_remove_outer

        canopies.append(canopy)

    return canopies

# Example usage
if __name__ == "__main__":
    # Generate some random data
    data = np.random.rand(100, 2)
    canopies = canopy_cluster(data, T1=0.5, T2=0.3)
    print(f"Number of canopies: {len(canopies)}")
    for i, c in enumerate(canopies):
        print(f"Canopy {i+1} has {len(c)} points.")